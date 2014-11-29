from tempodb import Client
from datetime import datetime
import urllib2, requests
import json
#client tempodb
tempodbClient=Client("7893765c91314ba5864feafcc41a12f2","6d8dddfc032d4482996d7398019d687e")
#client openWeatherMap

url="http://api.openweathermap.org/data/2.5/weather?q=Benney,fr&units=metric"
r=requests.get(url)
j=json.loads(r.text)
temperature = j['main']['temp']
humidity = j['main']['humidity']
wind=j['wind']['speed']
data = [
    { 'key': 'ExtTemperature', 'v': temperature },
    { 'key': 'Humidity', 'v': humidity },
{'key':'Wind','v':wind}
 ] 
tempodbClient.write_bulk(datetime.now(),data) 

