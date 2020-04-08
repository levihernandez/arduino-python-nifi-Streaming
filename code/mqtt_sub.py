# file: mqtt_sub.py
# MQTT Python: https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# SensorCode: https://create.arduino.cc/projecthub/techno_z/dht11-temperature-humidity-sensor-98b03b
# JsonCode: https://arduinojson.org/v6/example/generator/

import paho.mqtt.client as mqtt
import sys
import time

# Server config, port, topic
# localhost
host = sys.argv[1]
# 1883
port = int(sys.argv[2])
# "topic/iot"
topic = sys.argv[1]

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(topic)

def on_message(client, userdata, msg):
  if msg.payload.decode() == "Hello world!":
    print("Yes!")
    client.disconnect()
  else:
    print(msg.payload.decode())

client = mqtt.Client()
client.connect(host,port,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
