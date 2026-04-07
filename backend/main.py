import paho.mqtt.client as mqtt
import mysql.connector
import json
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

try:
    with open("../password.txt", "r") as file:
        mqtt_password = file.read().strip() 
except FileNotFoundError:
    print("Nie znaleziono plika password.txt!")
    exit()

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
        print("dotarla wiadomosc")
        data = json.loads(message.payload.decode("utf-8"))
        db = get_db_connection()
        cursor = db.cursor()

        #comfort obliczenia

        sql = "INSERT INTO measurements (sensor_id, temperature, humidity, co2, comfort_score) VALUES (%s, %s, %s, %s, %s)"
        values = (data['sensor_id'], data['temp'], data['hum'], data['co2'], 0)

        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()

        print(f"Saved data from: {data['sensor_id']}")

    except Exception as e:
        print(f"Error: {e}")

def on_connect(client, userdata, flags, rc):
    print("Połączono z brokerem MQTT")
    client.subscribe("akursa/microclimate/measurements")

def run_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("admin", mqtt_password)

    client.tls_set() 
    client.connect("e48e564e16c447268f3360c3098a0691.s1.eu.hivemq.cloud", 8883)
    
    client.loop_start() 
    while True:
        time.sleep(1)


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