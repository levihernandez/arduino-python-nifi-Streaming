#include <dht.h>
#include <ArduinoJson.h>

/*
KY-015 Temp+Humidity Sensor Module (Digital)
https://arduinomodules.info/ky-015-temperature-humidity-sensor-module/

KY-015  Arduino
------- -------
S Pin    8
middle  +5V
-       GND

# MQTT Python: https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# SensorCode: https://create.arduino.cc/projecthub/techno_z/dht11-temperature-humidity-sensor-98b03b
# JsonCode: https://arduinojson.org/v6/example/generator/
*/
#define dht_apin 8 // Analog Pin sensor is connected to

 
dht DHT;
char str[32]; 

void setup(){
 
  Serial.begin(9600);
  while (!Serial) continue;


  
  delay(500);//Delay to let system boot
  // Serial.println("DHT11 Humidity & temperature Sensor\n\n");
  delay(1000);//Wait before accessing Sensor
 
}//end "setup()"



void loop(){
  DHT.read11(dht_apin);
  
  
  //Start of Program 
  
//  doc["c"] = DHT.temperature, "*C";
//  doc["f"] = DHT.humidity;
  //doc["time"] = now();
  StaticJsonDocument<200> doc;

  doc["sensor"] = "iot";
  doc["c"] = DHT.temperature;
  doc["f"] = round(1.8*DHT.temperature+32);
  doc["humidity"] = DHT.humidity;
  //JsonArray data = doc.createNestedArray("data");
  // data.add(doc["temperature"] = DHT.temperature);
  // data.add(DHT.humidity);
    
    serializeJson(doc, Serial);
    Serial.println();
    
   
    delay(1000);//Wait 5 seconds before accessing sensor again.
 
  //Fastest should be once every two seconds.
 
}// end loop
