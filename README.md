# arduino-python-nifi-Streaming
Stream data from Arduino sensor to NiFi

> Manually publish "iot" topic in Mosquitto with mosquitto_pub or mqtt_pub.py custom script

```bash
pi@raspberrypi:~/Documents $ mosquitto_pub -h localhost -t "topic/iot" -m "{\"sensor\":\"iot\",\"c\":31,\"f\":88,\"humidity\":38}"

pi@raspberrypi:~/Documents $ python3 mqtt_pub.py localhost 1883 "topic/iot"
```

> Create service daemon for the python script

```bash
pi@raspberrypi:~/Documents $ sudo systemctl daemon-reload

pi@raspberrypi:~/Documents $ sudo systemctl status pyduino.service
● pyduino.service - PyDuino Service
   Loaded: loaded (/lib/systemd/system/pyduino.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
   
pi@raspberrypi:~/Documents $ sudo systemctl enable pyduino.service
Created symlink /etc/systemd/system/default.target.wants/pyduino.service → /lib/systemd/system/pyduino.service.

pi@raspberrypi:~/Documents $ sudo systemctl start pyduino.service

pi@raspberrypi:~/Documents $ sudo systemctl status pyduino.service
● pyduino.service - PyDuino Service
   Loaded: loaded (/lib/systemd/system/pyduino.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-04-08 12:51:52 EDT; 8s ago
 Main PID: 7116 (python3)
    Tasks: 1 (limit: 2200)
   Memory: 5.8M
   CGroup: /system.slice/pyduino.service
           └─7116 /usr/bin/python3 /home/pi/Documents/mqtt_pub.py localhost 1883 topic/iot

Apr 08 12:51:52 raspberrypi systemd[1]: Started PyDuino Service.
pi@raspberrypi:~/Documents $ ps -eaf | grep mqtt
root      7116     1  2 12:51 ?        00:00:00 /usr/bin/python3 /home/pi/Documents/mqtt_pub.py localhost 1883 topic/iot
pi        7134  4518  0 12:52 pts/0    00:00:00 grep --color=auto mqtt
```

> Subscribe to Mosquitto's "iot" topic with mosquitto_sub or custom mqtt_sub.py script

```bash
pi@raspberrypi:~/Documents $ mosquitto_sub -h localhost -t topic/iot -v
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}

pi@raspberrypi:~/Documents $ python3 mqtt_sub.py localhost 1883 topic/iot
```
