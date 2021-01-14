import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')

    response = client.post_text(
        botName = 'Coach',
        botAlias = 'lingling',
        userId = 'User',
        inputText = json.loads(event['body'])['messages'][0]['unstructured']['text']
        )
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
       
        'body':json.dumps(response["message"])
    }
