# arduino-python-nifi-Streaming

Connect an Arduino sensor to Raspberry Pi3 and capture data from the serial port with a python script. Publish the data to Mosquitto. On a separate server, Install NiFi, Flink, Airflow to stream data, manage script completion, and route records to temp dir.

## PyDuino Project
* Arduino
	* Connect Temperature/Humidity sensor to Arduino
	* Flash Arduino code
	* Connect Arduino to Raspberry Pi
* Raspberry Pi 3
	*  Enable remote connection via SSH
	* Install packages/dependencies
	* Install Mosquitto
	* Configure ports for inbound requests
* Ubuntu server
	* Apache NiFi
	* Apache Flink
	* Apache Airflow
	 
	 

## Arduino

* Connect Temperature/Humidity sensor to Arduino
	* Download the DHT library and upload it to Arduino > Sketch > Library
	* In Sketch Library find ArduinoJSON and install it
	* [Humidity-Temp Sensor Project](https://create.arduino.cc/projecthub/techno_z/dht11-temperature-humidity-sensor-98b03b)
* Flash Arduino code
	* [Temperature/Sensor](code/Arduino/PyDuino.ino)
* Connect Arduino to Raspberry Pi
	* Use USB from Arduino to Raspberry Pi 3

## Raspberry Pi 3

* `IP: 192.168.86.115`
*  Enable remote connection via SSH
	* Connect the Raspberry Pi to a monitor 
	* `username: pi`
	*  `password: raspberry`
	* update password for `pi` user
	* Configure SSH
		* Enter `sudo raspi-config` in a terminal window
		* Select `Interfacing Options`
		* Navigate to and select `SSH`
		* Choose `Yes`
		* Select `Ok`
		* Choose `Finish`
		* `pi@raspberrypi:~ $ sudo raspi-config`
		* remote SSH access is now enabled
* Install updates/packages/dependencies with `sudo apt-get update`
* I opted for remotely installing the remaining packages

```bash
jlhernandez$ ssh pi@192.168.86.115
Linux raspberrypi 4.19.97-v7+ #1294 SMP Thu Jan 30 13:15:58 GMT 2020 armv7l

Last login: Mon Mar 23 16:07:42 2020

pi@raspberrypi:~ $ cd Documents/
```

Note: in the event of ssh not working, install the ssh service `sudo apt-get install openssh-server`

* Install OpenJDK

```bash
pi@raspberrypi:~ sudo apt install openjdk-8-jdk

pi@raspberrypi:~ java -version
openjdk version "1.8.0_212"
OpenJDK Runtime Environment (build 1.8.0_212-8u212-b01-1+rpi1-b01)
OpenJDK Client VM (build 25.212-b01, mixed mode)
```

* Download Mosquitto

```bash
pi@raspberrypi:~/Documents $ sudo pip3 install paho-mqtt
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting paho-mqtt
  Downloading https://www.piwheels.org/simple/paho-mqtt/paho_mqtt-1.5.0-py3-none-any.whl (61kB)
    100%                                                                         | 61kB 183kB/s 
Installing collected packages: paho-mqtt
Successfully installed paho-mqtt-1.5.0
```

* List Mosquitto version available in apt


```bash
pi@raspberrypi:~/Documents $ apt list  mosquitto
Listing... Done
mosquitto/stable 1.5.7-1+deb10u1 armhf
```

* Install Mosquitto Server

```bash
pi@raspberrypi:~/Documents $ sudo apt-get install mosquitto
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
  libev4 libuv1 libwebsockets8
Suggested packages:
  apparmor
The following NEW packages will be installed:
  libev4 libuv1 libwebsockets8 mosquitto
0 upgraded, 4 newly installed, 0 to remove and 0 not upgraded.
Need to get 360 kB of archives.
After this operation, 799 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf libev4 armhf 1:4.25-1 [34.5 kB]
Get:2 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf libuv1 armhf 1.24.1-1 [96.7 kB]
Get:3 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf libwebsockets8 armhf 2.0.3-3 [85.6 kB]
Get:4 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf mosquitto armhf 1.5.7-1+deb10u1 [143 kB]
Fetched 360 kB in 4s (94.2 kB/s)   
Selecting previously unselected package libev4:armhf.
(Reading database ... 93527 files and directories currently installed.)
Preparing to unpack .../libev4_1%3a4.25-1_armhf.deb ...
Unpacking libev4:armhf (1:4.25-1) ...
Selecting previously unselected package libuv1:armhf.
Preparing to unpack .../libuv1_1.24.1-1_armhf.deb ...
Unpacking libuv1:armhf (1.24.1-1) ...
Selecting previously unselected package libwebsockets8:armhf.
Preparing to unpack .../libwebsockets8_2.0.3-3_armhf.deb ...
Unpacking libwebsockets8:armhf (2.0.3-3) ...
Selecting previously unselected package mosquitto.
Preparing to unpack .../mosquitto_1.5.7-1+deb10u1_armhf.deb ...
Unpacking mosquitto (1.5.7-1+deb10u1) ...
Setting up libev4:armhf (1:4.25-1) ...
Setting up libuv1:armhf (1.24.1-1) ...
Setting up libwebsockets8:armhf (2.0.3-3) ...
Setting up mosquitto (1.5.7-1+deb10u1) ...
Created symlink /etc/systemd/system/multi-user.target.wants/mosquitto.service  /lib/systemd/system/mosquitto.service.
Processing triggers for systemd (241-7~deb10u3+rpi1) ...
Processing triggers for man-db (2.8.5-2) ...
Processing triggers for libc-bin (2.28-10+rpi1) ...

pi@pi:~/Documents $ mosquitto -v
1586481407: mosquitto version 1.5.7 starting
1586481407: Using default config.
1586481407: Opening ipv4 listen socket on port 1883.
1586481407: Error: Address already in use

pi@raspberrypi:~/Documents $ systemctl status mosquitto
           mosquitto.service - Mosquitto MQTT v3.1/v3.1.1 Broker
   Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2020-03-23 20:41:14 EDT; 3min 16s ago
     Docs: man:mosquitto.conf(5)
           man:mosquitto(8)
 Main PID: 2418 (mosquitto)
    Tasks: 1 (limit: 2200)
   Memory: 672.0K
   CGroup: /system.slice/mosquitto.service
           2418 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

Mar 23 20:41:14 raspberrypi systemd[1]: Starting Mosquitto MQTT v3.1/v3.1.1 Broker...
Mar 23 20:41:14 raspberrypi systemd[1]: Started Mosquitto MQTT v3.1/v3.1.1 Broker.
```

* Install Mosquitto client Pub/Sub

```bash
pi@raspberrypi:~/Documents $ sudo apt-get install mosquitto-clients
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
  libmosquitto1
The following NEW packages will be installed:
  libmosquitto1 mosquitto-clients
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Need to get 124 kB of archives.
After this operation, 255 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf libmosquitto1 armhf 1.5.7-1+deb10u1 [57.6 kB]
Get:2 http://mirror.pit.teraswitch.com/raspbian/raspbian buster/main armhf mosquitto-clients armhf 1.5.7-1+deb10u1 [66.8 kB]
Fetched 124 kB in 3s (47.5 kB/s)            
Selecting previously unselected package libmosquitto1:armhf.
(Reading database ... 93576 files and directories currently installed.)
Preparing to unpack .../libmosquitto1_1.5.7-1+deb10u1_armhf.deb ...
Unpacking libmosquitto1:armhf (1.5.7-1+deb10u1) ...
Selecting previously unselected package mosquitto-clients.
Preparing to unpack .../mosquitto-clients_1.5.7-1+deb10u1_armhf.deb ...
Unpacking mosquitto-clients (1.5.7-1+deb10u1) ...
Setting up libmosquitto1:armhf (1.5.7-1+deb10u1) ...
Setting up mosquitto-clients (1.5.7-1+deb10u1) ...
Processing triggers for man-db (2.8.5-2) ...
Processing triggers for libc-bin (2.28-10+rpi1) ...
```

* Manually publish "iot" topic in Mosquitto with mosquitto_pub or mqtt_pub.py custom script, I followed the example from [Ingest & publish to MQTT](https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/) to build the python scripts.

```bash
pi@raspberrypi:~/Documents $ mosquitto_pub -h localhost -t "topic/iot" -m "{\"sensor\":\"iot\",\"c\":31,\"f\":88,\"humidity\":38}"

pi@raspberrypi:~/Documents $ python3 mqtt_pub.py localhost 1883 "topic/iot"
```

* Test Mosquitto Subscriber on a new terminal window, Subscribe to Mosquitto's "iot" topic with mosquitto_sub or custom mqtt_sub.py script

```bash

pi@raspberrypi:~/Documents $ mosquitto_sub -h localhost -t topic/iot -v
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}
topic/iot {"sensor":"iot","c":31,"f":88,"humidity":38}

pi@raspberrypi:~/Documents $ python3 mqtt_sub.py localhost 1883 topic/iot
```

### Create Daemon Service for Python3 Script

In the event of rebooting the Raspberry Pi 3 or power failure, register the script as a Daemon service to enable restart on boot.

* Create service file [python script agent](agent/pyduino.service)

Copy the contents of pyduino.service to `/lib/systemd/system/`. Note that the parameters, hostname and port, used by the Python publisher script are hardcoded in the service.

```bash
pi@raspberrypi:~ sudo vi /lib/systemd/system/pyduino.service
```

* Register the service, enable it, and run it

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

* Configure ports for inbound requests

```bash
pi@raspberrypi:~ sudo apt-get install ufw
pi@raspberrypi:~ sudo ufw allow 1883
pi@raspberrypi:~ 
```

## Ubuntu server

* Configure Ubuntu Server

```bash
jlhernandez@Levis ~ % ssh jlhernandez@ubuntu1804.local
Last login: Thu Apr  9 19:12:05 2020 from 192.168.86.189

jlhernandez@Ubuntu1804:~$ cd Documents/server
jlhernandez@Ubuntu1804:~$ sudo apt-get update
jlhernandez@Ubuntu1804:~$ sudo apt install openssh-server

jlhernandez@Ubuntu1804:~$ python3 --version
Python 3.6.9
```

	* Install pip3

```bash
jlhernandez@Ubuntu1804:~$ sudo apt install python3-pip
[sudo] password for jlhernandez: 
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:

jlhernandez@Ubuntu1804:~$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```

	* Install OpenJDK8

```bash
jlhernandez@Ubuntu1804:~$ sudo apt install openjdk-8-jre-headless
jlhernandez@Ubuntu1804:~$ java -version
openjdk version "1.8.0_242"
OpenJDK Runtime Environment (build 1.8.0_242-8u242-b08-0ubuntu3~18.04-b08)
OpenJDK 64-Bit Server VM (build 25.242-b08, mixed mode)
```
	* Disable Ubuntu GUI to preserve memory
	
```bash
jlhernandez@Ubuntu1804:~$ sudo systemctl set-default multi-user.target
jlhernandez@Ubuntu1804:~$ sudo reboot now
```

	* Open ports for NiFi, Flink, Airflow
	
```bash
# NiFi
jlhernandez@Ubuntu1804:~$ sudo ufw allow 8080
# Flink
jlhernandez@Ubuntu1804:~$ sudo ufw allow 8081
# Airflow
jlhernandez@Ubuntu1804:~$ sudo ufw allow 8082
```

* Apache NiFi `http://192.168.86.188:8080/nifi/`

```bash
jlhernandez@Ubuntu1804:~$ wget https://www.apache.org/dyn/closer.lua?path=/nifi/1.11.4/nifi-1.11.4-bin.tar.gz
jlhernandez@Ubuntu1804:~$ tar -xvf nifi-1.11.4-bin.tar.gz
jlhernandez@Ubuntu1804:~$ cd nifi-1.11.4
jlhernandez@Ubuntu1804:~$ bin/nifi.sh install
jlhernandez@Ubuntu1804:~$ sudo service nifi start
jlhernandez@Ubuntu1804:~$ sudo service nifi status
[sudo] password for jlhernandez: 
Warning: The unit file, source configuration file or drop-ins of nifi.service changed on disk. Run 'systemctl daemon-reload' to reload units.
● nifi.service - SYSV: Apache NiFi is a dataflow system based on the principles of Flow-Based Programming.
   Loaded: loaded (/etc/init.d/nifi; generated)
   Active: active (running) since Thu 2020-04-09 18:32:34 EDT; 2h 59min ago
     Docs: man:systemd-sysv-generator(8)
    Tasks: 117 (limit: 4915)
   CGroup: /system.slice/nifi.service
           ├─ 953 /bin/sh /home/jlhernandez/Documents/server/nifi/bin/nifi.sh start
           ├─ 955 /usr/bin/java -cp /home/jlhernandez/Documents/server/nifi/conf:/home/jlhernandez/Documents/server/nifi/lib/bootstrap/* -Xms12m -Xmx24m -Dorg.apache.nifi.b
           └─1190 java -classpath /home/jlhernandez/Documents/server/nifi/./conf:/home/jlhernandez/Documents/server/nifi/./lib/nifi-nar-utils-1.9.0.1.0.0.0-90.jar:/home/jlh

Apr 09 18:32:29 Ubuntu1804 systemd[1]: Starting SYSV: Apache NiFi is a dataflow system based on the principles of Flow-Based Programming....
Apr 09 18:32:30 Ubuntu1804 nifi[903]: nifi.sh: JAVA_HOME not set; results may vary
Apr 09 18:32:31 Ubuntu1804 nifi[903]: Java home:
Apr 09 18:32:31 Ubuntu1804 nifi[903]: NiFi home: /home/jlhernandez/Documents/server/nifi
Apr 09 18:32:31 Ubuntu1804 nifi[903]: Bootstrap Config File: /home/jlhernandez/Documents/server/nifi/conf/bootstrap.conf
Apr 09 18:32:34 Ubuntu1804 systemd[1]: Started SYSV: Apache NiFi is a dataflow system based on the principles of Flow-Based Programming..
```

* Apache Flink: `http://192.168.86.188:8081/#/overview`

```bash
jlhernandez@Ubuntu1804:~$ wget https://mirrors.sonic.net/apache/flink/flink-1.10.0/flink-1.10.0-bin-scala_2.12.tgz
jlhernandez@Ubuntu1804:~$ tar -xvf flink-1.10.0-bin-scala_2.12.tgz
jlhernandez@Ubuntu1804:~$ cd flink-1.10.0/
jlhernandez@Ubuntu1804:~$ bin/start-cluster.sh
```

* Apache Airflow: 

```bash
jlhernandez@Ubuntu1804:~$ pip3 install apache-airflow
Collecting apache-airflow

jlhernandez@Ubuntu1804:~$ pip3 install mysqlclient
jlhernandez@Ubuntu1804:~$ 
```

## NiFi subscription to Mosquitto

* In Mosquitto, chek the log to see if NiFi has connected to subscribe

```bash
pi@raspberrypi:~/Documents $ sudo tail -f /var/log/mosquitto/mosquitto.log
1585412250: Saving in-memory database to /var/lib/mosquitto/mosquitto.db.
1585414051: Saving in-memory database to /var/lib/mosquitto/mosquitto.db.
1585415852: Saving in-memory database to /var/lib/mosquitto/mosquitto.db.
1585416420: Socket error on client 51663694-d816-48bd-9d33-a28e521fad66, disconnecting.
1585416420: mosquitto version 1.5.7 terminating
1585416441: mosquitto version 1.5.7 starting
1585416441: Config loaded from /etc/mosquitto/mosquitto.conf.
1585416441: Opening ipv4 listen socket on port 1883.
1585416441: Opening ipv6 listen socket on port 1883.
```

* NiFi connected to Raspberry Pi

> Mosquitto log shows a new connection on port `1883` from NiFi with IP `192.168.86.188` and starts consuming the topic

`1585418002: New connection from 192.168.86.188 on port 1883.`

```bash
pi@raspberrypi:~/Documents $ sudo tail -f /var/log/mosquitto/mosquitto.log
1585416420: mosquitto version 1.5.7 terminating
1585416441: mosquitto version 1.5.7 starting
1585416441: Config loaded from /etc/mosquitto/mosquitto.conf.
1585416441: Opening ipv4 listen socket on port 1883.
1585416441: Opening ipv6 listen socket on port 1883.
1585418002: New connection from 192.168.86.188 on port 1883.
1585418002: New client connected from 192.168.86.188 as raspberry (c1, k60).
```

* On the NiFi server, use the  [PyDuino Workflow](code/NiFi/PyDuino.xml) route the PutFile processor to the NiFi /tmp/nifi dir, lets see the contents from the file flow

Files are now being stored in the file system temp directory.`

```bash
jlhernandez@Ubuntu1804:~/Documents/server$ ls -l /tmp/nifi/ | more
total 456
-rw-r--r-- 1 jlhernandez jlhernandez 44 Mar 28 13:58 0242618d-a055-45bf-a4e6-a5235cf20919
-rw-r--r-- 1 jlhernandez jlhernandez 44 Mar 28 13:58 0265a807-be12-446d-af0f-8a2080a1fe66
-rw-r--r-- 1 jlhernandez jlhernandez 44 Mar 28 13:58 0282d003-beae-43bc-b61a-1fa9c318e3b4
-rw-r--r-- 1 jlhernandez jlhernandez 44 Mar 28 13:58 073e8496-f508-4b44-8823-02881a9212f7
-rw-r--r-- 1 jlhernandez jlhernandez 44 Mar 28 13:59 085dde10-8542-4877-a529-9940d365c73b
```

* Preview the contents of the NiFi PutFile stored in `/tmp/nifi/` dir

The content of each file corresponds to a single output coming from the sensor.

```bash
jlhernandez@Ubuntu1804:~/Documents/server$ cat /tmp/nifi/0242618d-a055-45bf-a4e6-a5235cf20919
{"sensor":"iot","c":30,"f":86,"humidity":35}
```

## Install MySQL Server


