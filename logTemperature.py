#lecture en continu du capteur de temperature solaire
#ecriture des valeurs dans influxDB

from ConfigParser import SafeConfigParser
import serial
import logging
logging.basicConfig(filename='logTemperature.log',level=logging.DEBUG)

#Lecture de config.ini
parser = SafeConfigParser()
parser.read('config.ini')
url = parser.get('InfluxDB','url')
port = parser.get('InfluxDB', 'port')
username = parser.get('InfluxDB', 'username')
password = parser.get('InfluxDB', 'password')
database = parser.get('InfluxDB', 'database')

#Creation du client influxDB
from influxdb import client as influxdb
db = influxdb.InfluxDBClient(url, port , username, password, database)

#Lecture sur stick USB ENOcean
res=''
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

#GetTemperature sur capteur EnOcean xxx
def getTemperature(byteStr):
   if len(byteStr) != 24:
	return -1
   if ord(byteStr[0]) != 0x55:
	return -1
   if ord(byteStr[6]) != 0xA5:
	return -1
   return ord(byteStr[9])

while True:
    res = ser.read(100)
    temp = getTemperature(res)
    #print temp
    if(temp != -1):
	#conversion de la valeur lue en temperature
        temp = 40-0.1548627*temp-2
	print(temp)
	data = [
        	{"name":"TempSalon",
           	"columns":["value"],
           	"points":[[round(temp,2)]]
            	}
            	]
	#Ecriture dans InfluxDB
        try:
           db.write_points(data)
	except ErrorValue as err:
     	   logging.error(err)
