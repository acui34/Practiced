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
    db = boto3.resource('dynamodb', region_name='us-east-1')
    runtime= boto3.client('runtime.sagemaker')
    song_table = db.Table('Songs')
    
    songId = event["queryStringParameters"]['songId']
    
    try:
        query = song_table.get_item(Key={'Id':songId})
    except (ValueError, TypeError):
        print(ValueError, TypeError)
        query = song_table.get_item(Key={'Id':'1'})
    

    ENDPOINT_NAME = "sagemaker-scikit-learn-2020-12-28-17-03-40-141"
    input_val = float(query["Item"]["difficulty"])
    pred = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                    Body=json.dumps([[input_val]]))
                                   #Body=[float(json.dumps(query["Item"]["difficulty"],cls=DecimalEncoder))].reshape(-1, 1))
    practice_time_pred_result = json.loads(pred['Body'].read().decode())
    
    
    response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps({"item": query["Item"], "prac_time": practice_time_pred_result},cls=DecimalEncoder),
            "isBase64Encoded": False}
    print(response)
    
    return response
    
