#!/usr/bin/python

import Adafruit_DHT 
import time 
import json 
import requests 
import copy 
import commands
import sys
sys.path.append("..")
import config



def load_data(humidity, temperature):
    getuname = "uname -n"
    status ,UNAME = commands.getstatusoutput(getuname)
    if humidity is not None:
        humidity_data = {"endpoint": UNAME ,"metric": "DHT11.humidity","timestamp": ts ,"step":60,"value": humidity ,"counterType":"GAUGE","tags":"module=dht11"} 
        payload.append(copy.copy(humidity_data)) 
    if temperature is not None: 
        temperature_data = {"endpoint":UNAME,"metric": "DHT11.temperature","timestamp":ts,"step":60,"value":temperature,"counterType":"GAUGE","tags":"module=dht11"} 
        payload.append(copy.copy(temperature_data)) 


if __name__ == '__main__': 
    sensor = Adafruit_DHT.DHT11 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 04) 
    ts = int(time.time()) 
    push_url = "http://{}:1988/v1/push",format(config.falcon_config['api_ip']) 
    payload = [] 
    load_data(humidity, temperature)

    print payload
    r = requests.post(push_url, data=json.dumps(payload))
    print r.text
