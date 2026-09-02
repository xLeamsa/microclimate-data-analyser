import json
import os
import time

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()

print(f"Connecting to broker: {MQTT_BROKER}...")
client.connect(MQTT_BROKER, MQTT_PORT)

payload = {
    "sensor_id": "test-comfort-13",
    "temp": "22",
    "hum": "50.00",
    "co2": 1000,
}

print(f"Publishing to {MQTT_TOPIC}...")
info = client.publish(MQTT_TOPIC, json.dumps(payload))
info.wait_for_publish()

print("Message published")
time.sleep(1)
client.disconnect()
