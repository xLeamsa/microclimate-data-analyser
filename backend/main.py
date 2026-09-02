import json
import os
import threading
import time
from functools import wraps

import mysql.connector
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from fuzzy_logic import calculate_comfort

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "microclimate_db")

API_KEY = os.getenv("API_KEY")
OFFLINE_THRESHOLD_SECONDS = int(os.getenv("OFFLINE_THRESHOLD_SECONDS", "150"))

app = Flask(__name__)
CORS(app)


def require_api_key(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not API_KEY or request.headers.get("X-API-Key") != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return view_func(*args, **kwargs)

    return wrapper


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        comfort = calculate_comfort(data["temp"], data["hum"], data["co2"])

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO measurements (sensor_id, temperature, humidity, co2, comfort_score) "
            "VALUES (%s, %s, %s, %s, %s)",
            (data["sensor_id"], data["temp"], data["hum"], data["co2"], comfort),
        )
        db.commit()
        cursor.close()
        db.close()

        print(f"Saved measurement from: {data['sensor_id']}")
    except Exception as error:
        print(f"Error handling MQTT message: {error}")


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)


def run_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.tls_set()
    client.connect(MQTT_BROKER, MQTT_PORT)

    client.loop_start()
    while True:
        time.sleep(1)


@app.route("/api/measurements", methods=["GET"])
@require_api_key
def get_measurements():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 20")
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(results)


@app.route("/api/measurements/history", methods=["GET"])
@require_api_key
def get_history():
    time_range = request.args.get("range", "1d")

    hours = 24
    if time_range == "7d":
        hours = 24 * 7
    elif time_range == "30d":
        hours = 24 * 30

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT timestamp, temperature, humidity, co2, comfort_score "
        "FROM measurements "
        "WHERE timestamp >= NOW() - INTERVAL %s HOUR "
        "ORDER BY timestamp ASC",
        (hours,),
    )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)


@app.route("/api/status", methods=["GET"])
@require_api_key
def get_status():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT timestamp, TIMESTAMPDIFF(SECOND, timestamp, NOW()) AS seconds_since "
        "FROM measurements ORDER BY timestamp DESC LIMIT 1"
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()

    if not row:
        return jsonify({"online": False, "last_seen": None})

    online = row["seconds_since"] is not None and row["seconds_since"] <= OFFLINE_THRESHOLD_SECONDS
    return jsonify({"online": online, "last_seen": row["timestamp"].isoformat()})


if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=run_mqtt, daemon=True)
    mqtt_thread.start()

    print("Server API running on: http://127.0.0.1:5000/api/measurements")
    app.run(host="0.0.0.0", port=5000)