import serial
import logging
logging.basicConfig(filename='logTemperature.log',level=logging.DEBUG)


from influxdb import client as influxdb
db = influxdb.InfluxDBClient("193.55.104.132", 8086, "root", "root", "Loumanolkar")

res=''
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

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
    print temp
    if(temp != -1):
        temp = 40-0.1548627*temp-2
	print(temp)
	data = [
        	{"name":"TempSalon",
           	"columns":["Value"],
           	"points":[[round(temp,2)]]
            	}
            	]
#	print "Sending data"
        try:
           db.write_points(data)
	except ErrorValue as err:
     	   logging.error(err)
