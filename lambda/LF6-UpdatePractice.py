import json
from datetime import date
import time
import boto3
import random
from boto3.dynamodb.conditions import Key

import re


def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name='us-east-1')

    practice_list_table = db.Table('Practices')
   
    
    event = event["body"]
    print("EEE", event)

    event =json.loads(event)["message"]
    print("EA", event)
    
    
    input_username = event['username']
    input_songId = str(event['songId'])
    
    
    
    try:
        query = practice_list_table.get_item(Key={'username': input_username, 'songId': input_songId})
    except (ValueError, TypeError):
        print(ValueError, TypeError)
    
    message = ""
    today = date.today()
    
    if 'Item' in query.keys():
        finished = query['Item']['finished']
        practiceTime = query['Item']['practiceTime']
        startDate = query['Item']['startDate']
        songName = query['Item']['songName']
        
        if 'finished' in event:
            new_item = {
                'username': input_username, 
                'songId': input_songId,
                'finished': 1,
                'practiceTime': practiceTime,
                'startDate': startDate,
                'songName': songName,
                'endDate': today.strftime("%Y-%m-%d")}
            
            practice_list_table.put_item(Item=new_item)
            message = "successfully finish practice"
       
        elif 'practiceTime' in event:
    
            new_item = {
                'username': input_username, 
                'songId': input_songId,
                'finished': finished,
                'practiceTime': practiceTime + event['practiceTime'],
                'startDate': startDate,
                'songName': songName
            }
            practice_list_table.put_item(Item=new_item)
            
            message = "successfully update pratice time"
        
        else:
            message = "nothing happened"
            
        
    else:

        message = "Something is wrong! Try again later!"
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(message)
    }