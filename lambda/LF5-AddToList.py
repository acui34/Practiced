import json
from datetime import date
import time
import boto3
import random
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name='us-east-1')
    practice_list_table = db.Table('Practices')
    song_table = db.Table('Songs')
    input_username = event['message']['username']
    input_songId = event['message']['songId']
    
    try:
        query = song_table.get_item(Key={'Id':input_songId})
    except (ValueError, TypeError):
        print(ValueError, TypeError)
        query = song_table.get_item(Key={'Id':'1'})
        
    songName = query["Item"]["name"]
    
    try:
        query = practice_list_table.get_item(Key={'username': input_username, 'songId': input_songId})
    except (ValueError, TypeError):
        print(ValueError, TypeError)
    
    message = ""
    today = date.today()
    
    if 'Item' in query.keys():
        message = "This songs is already in your list!"
    else:
        new_item = {
            'username': input_username, 
            'songId': input_songId,
            'finished': 0,
            'practiceTime': 0,
            'startDate': today.strftime("%Y-%m-%d"),
            "songName": songName
        }
        practice_list_table.put_item(Item=new_item)
        message = "Sucessfully added it to practice list!"
        
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }