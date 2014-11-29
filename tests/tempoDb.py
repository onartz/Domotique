from tempodb import Client
#from datetime import datetime
import json
import datetime
#client TempoDB
tempoDbClient=Client("7893765c91314ba5864feafcc41a12f2","6d8dddfc032d4482996d7398019d687e")
tags = ["Delete"]

#summary = tempoDbClient.delete_series(tags=tags)
#summary=tempoDbClient.create_series("TEMP1")

start = datetime.datetime(2014, 1, 1)
end = datetime.datetime(2014, 3, 2)

response = tempoDbClient.delete_key("TEMP1", start, end)
