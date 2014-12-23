from datetime import datetime
from ConfigParser import SafeConfigParser
import urllib2, requests
import json
import sys
import logging

configFile = '/home/pi/SmartHome/config.ini'
logFile = '/home/pi/SmartHome/logMeteo.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s %(message)s' )

logging.debug("Starting logMeteo.py")

#from pprint import pprint
from influxdb import client as influxdb

#Lecture de config.ini
parser = SafeConfigParser()
parser.read(configFile)
url = parser.get('InfluxDB','url')
port = parser.get('InfluxDB', 'port')
username = parser.get('InfluxDB', 'username')
password = parser.get('InfluxDB', 'password')
database = parser.get('InfluxDB', 'database')

#Client influxDB
db = influxdb.InfluxDBClient(url, port , username, password, database)

#client openWeatherMap
openWeatherMapUrl = parser.get('OpenWeatherMap', 'url') 
logging.info(openWeatherMapUrl)

try:
  r=requests.get(openWeatherMapUrl)
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
  logging.info(data)

  db.write_points(data)
except ValueError as err:
  logging.error(err)
 
 

