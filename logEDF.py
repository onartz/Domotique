from datetime import datetime
import urllib2, requests
import json
from influxdb import client as influxdb
db = influxdb.InfluxDBClient("sandbox.influxdb.com", 8086, "Loumanolkar", "Olkaman1!", "Loumanolkar")
url="http://192.168.0.13/json"
r=requests.get(url)
str=(r.text).replace("&quot;",'"');
j=json.loads(str)

HP = j['HP']
HC = j['HC']
IMAX = j['IMAX']
data = [
    {"name":"HP","columns":["value"],"points":[[HP]]},
    {"name":"HC","columns":["value"],"points":[[HC]]},
    {"name":"IMAX","columns":["value"],"points":[[IMAX]]}
       ]
db.write_points(data)

