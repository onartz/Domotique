import socket
import struct
import json
import smtplib
from influxdb import client as influxdb
db = influxdb.InfluxDBClient("sandbox.influxdb.com", 8086, "Loumanolkar", "Olkaman1!", "Loumanolkar")

from pprint import pprint

MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1234

START = 0
WAITING = 1
ERROR = 2 
newstate = 1

#Etat initial
state = START
def sendEmail():
   to = 'olivier.nartz@gmail.com'
   gmail_user = 'olivier.nartz@gmail.com'
   gmail_pwd = 'Olkaman1!'
   smtpserver = smtplib.SMTP("smtp.gmail.com",587)
   smtpserver.ehlo()
   smtpserver.starttls()
   smtpserver.ehlo
   smtpserver.login(gmail_user, gmail_pwd)
   header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Compteur absent \n'
   print header
   msg = header + '\n Alerte compteur absent \n\n'
   smtpserver.sendmail(gmail_user, to, msg)
   print 'done!'
   smtpserver.close()



#Fonction setState
def setState(pState):
   global state
   state=pState
   newstate=1

#Fonction de sauvegarde InfluxDB
def save(pData):
   j=json.loads(pData)
   del j["nberreurs"]
   del j["nblectureOK"]
   s='[' + str(j) + ']'
   #s+=str(j)
   #s+=']'
   s = s.replace("u'", "'")
   s = s.replace("'",'"')
   db.write_points(s)


#Debut
#Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#On met un timeout sur la reception
sock.settimeout(2)

#On rejoint le groupe
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
 
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)



while True:
   if state == START:
      if newstate == 1:
        print "entering START"
        setState(WAITING)
   if state == WAITING:
      if newstate == 1:
         newstate = 0
         sock.settimeout(120)
         print "Entering Waiting"
      try:
         data, addr = sock.recvfrom(512)
         save(data)
      except:
         state = ERROR
         newstate = 1
   if state == ERROR:
      if newstate == 1:
         newstate = 0
         print "Entering Error"
         sock.settimeout(None)     
      data, addr = sock.recvfrom(512)
      save(data)
      setState(WAITING)

