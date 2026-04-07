import paho.mqtt.client as mqtt
import json
import time

BROKER = "e48e564e16c447268f3360c3098a0691.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "akursa/microclimate/measurements"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

client.username_pw_set("admin", "Admin123")

client.tls_set()

print(f"Łączenie z prywatnym brokerem: {BROKER}...")
client.connect(BROKER, PORT)

data = {
    "sensor_id": "test3",
    "temp": "25.10",    
    "hum": "45.00",    
    "co2": 750
}

print(f"Wysyłam dane na temat: {TOPIC}...")
info = client.publish(TOPIC, json.dumps(data))
info.wait_for_publish() 

print("Dane wysłane do prywatnej chmury")
time.sleep(1) 
client.disconnect()