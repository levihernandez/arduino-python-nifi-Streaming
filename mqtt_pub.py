# file: mqtt_pub.py
# MQTT Python: https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# SensorCode: https://create.arduino.cc/projecthub/techno_z/dht11-temperature-humidity-sensor-98b03b
# JsonCode: https://arduinojson.org/v6/example/generator/

import paho.mqtt.client as mqtt
import time
import serial
import RPi.GPIO as GPIO
import sys

# SYNTAX: python3 localhost 1883 "topic/iot"
# localhost
host = sys.argv[1]
# 1883
port = int(sys.argv[2])
# "topic/iot"
topic = sys.argv[3]
# "ttyACM0
# srl = sys.argv[4]

#change ACM number as found from ls /dev/tty/ACM*
ser=serial.Serial("/dev/ttyACM0",9600)  

client = mqtt.Client()
client.connect(host,port,60)

while True:

    rd_line=ser.readline()
    str_rn = rd_line.decode()
    str_fmt = str_rn.rstrip()
    client.publish(topic,str_fmt);

client.disconnect();
