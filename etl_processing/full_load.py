
from wsgiref import headers
import pandas as pd
import json
import datetime
import requests

credentials = json.load(open("./credentials.json"))
USER_ID = credentials['user_id']
TOKEN = credentials["token"]

def consult_full_load(df,headers):
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?before={}".format(df["api_ref"].tail(1).values[0]), headers = headers).json()
    
    songs = []
    artists = []
    playeds = []
    timestamps = []
    api_ref = []
    if r == None:
        return df
    for i in r.get('items'):
        songs.append(i['track']['name'])
        artists.append(i["track"]["album"]["artists"][0]["name"])
        playeds.append(i["played_at"])
        timestamps.append(i["played_at"][0:10])
        api_ref.append(r.get('next')[-13:])

    only_df = pd.DataFrame(columns=['song_name', 'artist', 'player','date','api_ref'] ,data= zip(songs, artists, playeds, timestamps,api_ref))

    df.append(only_df)    
    return df

def extract_api_spotify(request):
    songs = []
    artists = []
    playeds = []
    timestamps = []
    api_ref = []
    for i in r.get('items'):
        songs.append(i['track']['name'])
        artists.append(i["track"]["album"]["artists"][0]["name"])
        playeds.append(i["played_at"])
        timestamps.append(i["played_at"][0:10])
        api_ref.append(r.get('next')[-13:])    

    
    df = pd.DataFrame(columns=['song_name', 'artist', 'player','date','api_ref'] ,data= zip(songs, artists, playeds, timestamps,api_ref))

    return df

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
          
  
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?before=1653348503117", headers = headers).json()
    #                  https://api.spotify.com/v1/me/player/recently-played?before=1651620847342
    #r = json.load(open("teste.json"))

    df = extract_api_spotify(r)
    
    while r != None:
        df = consult_full_load(df,headers)
    
    df.to_csv("teste.csv")
    
    
