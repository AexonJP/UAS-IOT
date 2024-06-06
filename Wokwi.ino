//Reference: https://youtu.be/XciKNSVWDiA?si=Ofxm7ttD9bIykHRJ
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Wokwi-GUEST";
const char* pass = "";

const char *mqtt_broker = "13.213.149.88";
const char *topicMQTTX = "weather/control";
const char *mqtt_username = "";
const char *mqtt_password = "";
const int mqtt_port = 1883;

const int LED_PIN = 16;
const int BUZ_PIN = 17;

WiFiClient espClient;
PubSubClient client(espClient);
int pos = 0;

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    String clientId = "mqttx_pa_group6";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("Connected");
      client.subscribe(topicMQTTX);
    } else {
      delay(5000);
    }
  }
}

void setup() {

  Serial.begin(9600);
  randomSeed(micros());
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZ_PIN, OUTPUT);


  setup_wifi();
  // Connecting to an MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Receive Topic: ");
  Serial.println(topic);
  String data = "";  // variabel untuk menyimpan data yang berbentuk array char
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    data += (char)payload[i];  // menyimpan kumpulan char kedalam string
  }
  Serial.print("Payload: ");
  Serial.println(data);
  
  if (strcmp(topic, topicMQTTX) == 0) {
    if (data == "ON") {
      digitalWrite(LED_PIN, HIGH);
    } else if (data == "OFF")  {
      digitalWrite(LED_PIN, LOW);
    }
    if (data == "OPEN") {
      digitalWrite(BUZ_PIN, HIGH);
    } else if (data == "CLOSE")  {
      digitalWrite(BUZ_PIN, LOW);
    }
  }
}


void loop() {
   if (!client.connected()) {
    reconnect();
  }
  client.loop();
}