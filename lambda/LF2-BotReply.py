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

def lambda_handler(event, context):
  
  if event['currentIntent']['name'] == "PracticeAdvice":
      res = recommendation_intent(event)
  else:
    res = {
        "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": "Glad to help!"
          }
        }
      }
  return res
  

def recommendation_intent(event):
  
  instrument = event['currentIntent']['slots']['Instrument']
  type = event['currentIntent']['slots']['Type']
  artist = event['currentIntent']['slots']['Artist']
  
  merged_query = " ".join([instrument,type,artist])
  
  elastic_response = query_elastic(type)
  
  msg = "Lets see... Hmm I'm not sure. Why don't you check out the search function?"
  
  if  elastic_response != []:
    songName = elastic_response[0]["_source"]['name']
    artistName = elastic_response[0]["_source"]['artist']
    youtube = elastic_response[0]["_source"]['youtube']
    
    msg = f"Great! Have you heard of {songName} by {artistName}? You can check this song at https://www.youtube.com/watch?v={youtube}!"
  
  res = {
        "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": msg,
          }
        }
    }
  return res
  
  
  

    
    
