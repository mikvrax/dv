#!/usr/bin/python3

import urllib.request
import json
import time

f = open("songs8.csv","r")
songs = f.readlines()
f.close()

url = 'https://api.spotify.com/v1/'
query1 = 'search?q=' 
query2 = 'audio-features/'


c = 0
out = open("audio_features9.csv","w")
for i in range(0,len(songs)):
    c = c + 1
    song = songs[i]
    song = song.replace(" ","%20")
    song = song.replace("\n","")
    try:   
        auth = urllib.request.Request(url+query1+song+'&type=track',headers={'Authorization': 'Bearer BQBh4QFjk7s9xntzkiH2YmtUW11GSExAX3j3LbVjviGkwWi1QmztW7ExIdj872zUox43Imnxl-nLCq8igu_DHPOVnUNaYOBb3whmo76yr0iTtj7vpmRD_JNHyWvShMvqqPbL-wdjnPfAM1IP7YsraGbynXtyFetVxM0IZxQ'})
        response = urllib.request.urlopen(auth)
        sleeptime = response.headers['X-Rate-Limit-Reset']
        response = response.read()
        try:
           data = json.loads(response.decode("utf-8"))
        except ValueError as e:
            print("Problem decoding response for id of " + song)
            print(e)
        if data['tracks']['items'] == []:
            print("Didn't find id for " + song + " number " + str(c))
            continue
        else:
            song_id = data['tracks']['items'][0]['id']
        time.sleep(int(sleeptime))
    except urllib.error.URLError as e:
        print("Didn't download id for " + song + " number " + str(c))
        print(e)
        continue
    try:

        auth = urllib.request.Request(url+query2+song_id ,headers={'Authorization': 'Bearer BQBh4QFjk7s9xntzkiH2YmtUW11GSExAX3j3LbVjviGkwWi1QmztW7ExIdj872zUox43Imnxl-nLCq8igu_DHPOVnUNaYOBb3whmo76yr0iTtj7vpmRD_JNHyWvShMvqqPbL-wdjnPfAM1IP7YsraGbynXtyFetVxM0IZxQ'})

        response = urllib.request.urlopen(auth)
        sleeptime = response.headers['X-Rate-Limit-Reset']
        response = response.read()
        try:
           data = json.loads(response.decode("utf-8"))
        except ValueError as e:
            print("Problem decoding response for features of" + song)
            print(e)
        out.write(str(data["danceability"])+',')
        out.write(str(data["energy"])+',')
        out.write(str(data["key"])+',')
        out.write(str(data["loudness"])+',')
        out.write(str(data["mode"])+',')
        out.write(str(data["speechiness"])+',')
        out.write(str(data["acousticness"])+',')
        out.write(str(data["instrumentalness"])+',')
        out.write(str(data["liveness"])+',')
        out.write(str(data["valence"])+',')
        out.write(str(data["tempo"])+',')
        out.write(str(data["type"])+',')
        out.write(str(data["duration_ms"])+',')
        out.write(str(data["time_signature"])+'\n')
        time.sleep(int(sleeptime))
    except urllib.error.URLError as e:
        print("Didn't download results for features of " + song + " number " + str(c)) 
        continue
    print(song)

out.close()

