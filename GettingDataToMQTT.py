
# python 3.11

import random
import time
import json
import requests

from paho.mqtt import client as mqtt_client


broker = '13.213.149.88'
port = 1883
topic = "bagus/ok"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # msg_count = 1
    while(True):
        url = ("https://platform.antares.id:8443/~/antares-cse/antares-id/AQWM/weather_airQuality_nodeCore_teknik?lim=20&fu=1&drt=2&ty=4")
        header = {"Accept":"application/json",
        "X-M2M-Origin":"ee8d16c4466b58e1:3b8d814324c84c89",
        "Content-Type":"application/json"}
        ok= requests.get(url=url, headers=header)
        # print((ok.text).replace("'", '"'))
        #with open("C:/Games/data.txt" , 'w') as f:
        #    f.write((ok.text).replace("'", '"'))
        # print(data)
        data = json.loads((ok.text).replace("'", '"'))
        print(data["m2m:list"][0]['m2m:cin']['con'])
        data = data["m2m:list"][0]['m2m:cin']['con']
        # print(type(data))
        data = json.loads(data)
        for key, value in data.items():
            try:
                if key == "Temp" :
                    value = str(value)
                    value = value[0:value.find(".")+2]
                    print("value temp",value)
                elif key == "AQI":
                    value = str(value)
                    if len(value) > 3:
                        value = value[0:3]
                elif key == "Hum":
                    value = str(value)
                    value = value[0:value.find(".")+3]
                elif key == "PM10":
                    value = str(value)
                    if len(value) > 3:
                        value = value[0:3]
                elif key == "Ozon":
                    value = str(value)
                    value = value[0:value.find(".")+3]
                elif key == "Lux":
                    value = str(value)
                    value = value[0:value.find(".")]
                msg = f"{value}"
                client.publish(f"weather/{key}", msg)
            except:
                msg = f"{value}"
                client.publish(f"weather/{key}", msg)
            
        time.sleep(5)
    # while True:
    #     time.sleep(1)
    #     msg = f"messages: {msg_count}"
    #     result = client.publish(topic, msg)
    #     # result: [0, 1]
    #     status = result[0]
    #     if status == 0:
    #         print(f"Send `{msg}` to topic `{topic}`")
    #     else:
    #         print(f"Failed to send message to topic {topic}")
    #     msg_count += 1
    #     if msg_count > 5:
    #         break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()