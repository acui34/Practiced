import json
from datetime import datetime 
import time 
import boto3
import random
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    db = boto3.client('dynamodb')
    username = event["queryStringParameters"]['username']
    
    try:
        query = db.query(
            TableName='Practices',
            KeyConditionExpression='username = :username',
            ExpressionAttributeValues={
                ':username': {'S': username}
            }
        )
    except (ValueError, TypeError):
        print(ValueError, TypeError)
        
    response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(query,cls=DecimalEncoder),
            "isBase64Encoded": False}

    return response