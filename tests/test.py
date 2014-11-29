import serial
#from tempodb import Client
#from datetime import datetime
#import urllib2, requests
import json

#client TempoDB
#tempoDbClient=Client("7893765c91314ba5864feafcc41a12f2","6d8dddfc032d4482996d7398019d687e")

res=''
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

def ByteToHex( byteStr ):
   if byteStr is '':
	return 'vide'
   else:
   	return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()
while True:
    print ByteToHex(ser.read(100))
