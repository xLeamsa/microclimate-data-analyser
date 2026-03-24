import paho.mqtt.client as mqtt
import mysql.connector
import json
from flask import Flask, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# XAMPP
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="microclimate_db"
    )


# do wiadomosci z mqtt
def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        db = get_db_connection()
        cursor = db.cursor()

        sql = "INSERT INTO measurements (sensor_id, temperature, humidity, co2, comfort_score) VALUES (%s, %s, %s, %s, %s)"
        values = (data['sensor_id'], data['temp'], data['hum'], data['co2'], 0)

        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()

        print(f"Saved data from: {data['sensor_id']}")

    except Exception as e:
        print(f"Error: {e}")


def run_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("climate/measurements")
    client.loop_forever()


@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 20")
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(results)


if __name__ == '__main__':
    #osobne watki do pracy mqtt i flaska
    mqtt_thread = threading.Thread(target=run_mqtt)
    mqtt_thread.daemon = True #poprawne zamykanie
    mqtt_thread.start()

    print("Server API working on: http://127.0.0.1:5000/api/measurements")
    app.run(port=5000)