import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from boto3.dynamodb.conditions import Key
import random


def get_elastic_instance():
    host = 'search-search-song-jjfupz7xeoilclhrsmcww4mxvu.us-east-1.es.amazonaws.com'
    region = 'us-east-1'

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key,credentials.secret_key,region,service,session_token=credentials.token)
    es = Elasticsearch(
        hosts=[{'host':host, 'port':443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
    return es

def query_elastic(query):
    es = get_elastic_instance()
    response = es.search(index = "songs",
                body={
                  "query": {
                    "multi_match": {
                        "query": query,
                        "type": "phrase",
                        "fields": [
                            "name^3", 
                            "artist^1.5",
                            "tags^1.5"
                        ]
                    }
                 }
                }
                )
    res = response['hits']['hits']
    return res
    

def lambda_handler(event,context):

    query = event["queryStringParameters"]["q"]
    print("Query got")
    elastic_response = query_elastic(query)
    print("Searched",elastic_response)
        
    response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(elastic_response),
            "isBase64Encoded": False}

    return response