import json
import boto3
import pandas as pd

def upload_bucket(client_s3):
    client_s3.upload_file(Bucket='spotify-datalake-sample', Filename="./archive.csv", Key=f'raw/gfull_load/archive.csv')

client_s3 = boto3.client('s3')
upload_bucket(client_s3)



