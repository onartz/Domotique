from datetime import datetime
import urllib2, requests
import json
import sys

import logging
logging.basicConfig(filename='logMeteo.log',level=logging.DEBUG)

from pprint import pprint
from influxdb import client as influxdb
#Client influxDB
db = influxdb.InfluxDBClient("193.55.104.132",8086 , "root", "root", "Loumanolkar")
#client openWeatherMap

url="http://api.openweathermap.org/data/2.5/weather?q=Bayon,fr&units=metric"
try:
  r=requests.get(url)
except requests.exceptions.RequestException as err:
  logging.error(err)
  sys.exit()
if r.status_code != requests.codes.ok:
   logging.error("Error in URL")
   sys.exit()
try:
   j=json.loads(r.text)
except ValueError as err:
  logging.error(err)
  sys.exit()

try:
  temperature = j['main']['temp']
  humidity = j['main']['humidity']
  wind=j['wind']['speed']
  data = [
  {
    "name" : "ExtTemperature",
    "columns" : ["value"],
    "points" : [
      [temperature]
    ]
  },
  {
    "name" : "Humidity",
    "columns" : ["value"],
    "points" : [
      [humidity]
    ]
  },
  {
    "name" : "Wind",
    "columns" : ["value"],
    "points" : [
      [wind]
    ]
  }
  ]
  db.write_points(data)
except ValueError as err:
  logging.error(err)
 
 

