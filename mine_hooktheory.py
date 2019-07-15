#!/usr/bin/python3

import urllib.request
import json
import time

f = open("chords.txt","r")
f.readline()
chords = f.readlines()

url = 'https://api.hooktheory.com/v1/'
query = 'trends/songs?cp=' 
ids = []

for chord in chords:
   fields = chord.split(",")
   nl = fields[3].index("\n")
   ids.append(fields[3][:nl])


for i in ids:
   for j in ids:
      for q in ids:
         a = i.replace("/","\\")
         b = j.replace("/","\\")
         c = q.replace("/","\\")         
         filename = 'results/chordprogresion'+a+","+b+","+c+".json"
         out = open(filename, 'w')
         for k in range(1,200):
            try:   
               auth = urllib.request.Request(url+query+i+","+j+','+c+"&page="+str(k),headers={'Authorization': 'Bearer bf8af837edea621da295d62a433be8ee'} )
               response = urllib.request.urlopen(auth)
               sleeptime = response.headers['X-Rate-Limit-Reset']
               response = response.read()
               if (len(response) == 2) or (response == b'No songs match this chord progression'):
                  print("No more results for " + i + "," + j + "," + q+" after page " + str(k))
                  break
               try:
                  data = json.loads(response.decode("utf-8"))
                  json.dump(data, out)
               except ValueError as e:
                  print("Problem with results for " + i + "," + j + ","+ q+" after page " + str(k))
                  print(e)
               time.sleep(int(sleeptime))
            except urllib.error.URLError as e:
               print("Didn't download results for " + i + "," + j +","+q+ " page " + str(k))
               continue
         out.close()

