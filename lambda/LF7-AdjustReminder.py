import json
from datetime import date
import time
import boto3
import random
import re
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name='us-east-1')
    practice_list_table = db.Table('Practices')
    reminder_table = db.Table('Reminders')
    event = event["body"]


    event =json.loads(event)["message"]
    print("EA", event)
    
    input_username = event['username']
    input_email = event['useremail']
    
    try:
        query = reminder_table.get_item(Key={'username':input_username})
    except (ValueError, TypeError):
        print(ValueError, TypeError)
        
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    message = ""
    
    if not re.search(regex,input_email):
         message = "Please enter a valid email address."
    elif 'Item' in query.keys():
        message = "You have already subscribed to daily reminder."
    else:
        new_item = {
            'username': input_username, 
            'email': input_email,
        }
        reminder_table.put_item(Item=new_item)
        message = "You have successfully subscribed to daily reminder!"
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(message)
    }