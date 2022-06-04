
import pandas as pd
import json
import datetime
import requests
import boto3

credentials = json.load(open("./credentials.json"))
USER_ID = credentials['user_id']
TOKEN = credentials["token"]
s3_client = boto3.client('s3')

def batch(df,s3_client):
    filename = f"{str(datetime.datetime.today().date())}.csv"
    df.to_csv(filename)
    s3_client.upload_file(Bucket='spotify-datalake-sample', Filename=f"./{filename}", Key=f'raw/incremental/')
    return True

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
          

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers).json()   

    df = extract_api_spotify(r)

    if df.empty:
        print("Empty")
    else:
        batch(df,s3_client)

        


    

    
