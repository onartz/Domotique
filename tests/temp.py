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
   if len(byteStr) != 24:
	return 'Bad size'
   if byteStr is '':
	return 'vide'
   print ord(byteStr[6])
   if ord(byteStr[6]) != 165:
	return 'Not a temperature'
   
   else:
	print len(byteStr)
	if byteStr[0] == 55 :
		str = byteStr[9]
		return ''.join(["%02X" % ord(str)]).strip()
	else :
		return 'unknown'
   	#return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()
while True:
    print ByteToHex(ser.read(100))
