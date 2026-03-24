import paho.mqtt.client as mqtt
import json
import time

BROKER = "broker.hivemq.com"
TOPIC = "akursa/microclimate/measurements"

client = mqtt.Client()
client.connect(BROKER, 1883)

data = {
    "sensor_id": "Test_2",
    "temp": "21.50",    
    "hum": "40.00",    
    "co2": 600
}


print(f"Wysyłam dane na temat: {TOPIC}...")
info = client.publish(TOPIC, json.dumps(data))
info.wait_for_publish() 
print("Sukces! Dane wysłane.")
time.sleep(1) 
client.disconnect()