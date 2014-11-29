from tempodb import Client
from datetime import datetime
import urllib2, requests
import json
#client tempodb
tempodbClient=Client("7893765c91314ba5864feafcc41a12f2","6d8dddfc032d4482996d7398019d687e")
#client openWeatherMap

url="http://192.168.0.13/json"
r=requests.get(url)
str=(r.text).replace("&quot;",'"');
j=json.loads(str)

HP = j['HP']
HC = j['HC']
IMAX = j['IMAX']
data = [
    { 'key': 'HP', 'v': HP },
    { 'key': 'HC', 'v': HC },
{'key':'IMAX','v':IMAX}
 ] 
tempodbClient.write_bulk(datetime.now(),data) 

