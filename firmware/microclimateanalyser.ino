#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include "DFRobot_ENS160.h"
#include "secrets.h"

const char* WIFI_SSID = SECRET_SSID;
const char* WIFI_PASSWORD = SECRET_PASS;

const char* MQTT_BROKER = "e48e564e16c447268f3360c3098a0691.s1.eu.hivemq.cloud";
const int MQTT_PORT = 8883;
const char* MQTT_USER = SECRET_MQTT_USER;
const char* MQTT_PASSWORD = SECRET_MQTT_PASS;
const char* MQTT_TOPIC = "akursa/microclimate/measurements";
const char* SENSOR_ID = "ESP32_Room_1";

const uint32_t PUBLISH_INTERVAL_MS = 60000;
const uint16_t CO2_FALLBACK_PPM = 400;

WiFiClientSecure secureClient;
PubSubClient mqttClient(secureClient);
Adafruit_BME280 bme;
DFRobot_ENS160_I2C ens160(&Wire, 0x53);

unsigned long lastPublish = 0;

void connectWifi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void connectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT broker...");

    String clientId = "ESP32Client-" + String(random(0, 0xffff), HEX);

    if (mqttClient.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("Connected to HiveMQ Cloud");
    } else {
      Serial.print("Connection failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" - retrying in 5s");
      delay(5000);
    }
  }
}

uint16_t readCo2() {
  uint8_t status = ens160.getENS160Status();

  switch (status) {
    case 0:
      return ens160.getECO2();
    case 1:
      Serial.println("ENS160 warming up");
      return CO2_FALLBACK_PPM;
    default:
      Serial.println("ENS160 error or not ready");
      return CO2_FALLBACK_PPM;
  }
}

void publishMeasurement() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  uint16_t co2 = readCo2();

  StaticJsonDocument<200> payload;
  payload["sensor_id"] = SENSOR_ID;
  payload["temp"] = String(temperature, 2);
  payload["hum"] = String(humidity, 2);
  payload["co2"] = co2;

  char buffer[200];
  serializeJson(payload, buffer);

  Serial.print("Publishing: ");
  Serial.println(buffer);

  if (mqttClient.publish(MQTT_TOPIC, buffer)) {
    Serial.println("Message delivered");
  } else {
    Serial.println("MQTT publish failed");
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!bme.begin(0x76)) {
    Serial.println("BME280 not found");
  }

  while (ens160.begin() != 0) {
    Serial.println("ENS160 not found");
    delay(1000);
  }

  ens160.setPWRMode(ENS160_SLEEP_MODE);
  delay(100);
  ens160.setPWRMode(ENS160_STANDARD_MODE);

  connectWifi();

  secureClient.setInsecure();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (!mqttClient.connected()) {
    connectMqtt();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish > PUBLISH_INTERVAL_MS) {
    lastPublish = now;
    publishMeasurement();
  }
}
