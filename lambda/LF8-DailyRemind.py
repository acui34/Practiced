import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    db = boto3.resource('dynamodb', region_name='us-east-1')
    reminders_table = db.Table('Reminders')

    sns = boto3.client('sns', region_name='us-east-1')
    # The character encoding for the email.
    CHARSET = "UTF-8"
    SENDER = "aiqic98@gmail.com"
    SUBJECT = "Daily Practice Remminder"
    CONFIGURATION_SET = "ConfigSet"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name='us-east-1') 
    
    
    response = reminders_table.scan()
    print("RRR",response)
    
    if 'Items' in response:
        print("Table not empty")
        items = response['Items']
        for item in items:
            email = item['email']
            name = item['username']
            
            message_to_user = f"Dear {name}, this is a reminder for you from Practiced.com! Please don't forget to practice today :)"
            
            BODY_TEXT = (message_to_user)
                        
            
            BODY_HTML = f"""<html>
            <head></head>
            <body>
              <h1>Have you practiced today?</h1>
              <p>{message_to_user}</p>
            </body>
            </html>
                        """   
            try:
                #Provide the contents of the email.
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            email,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source=SENDER
                    # If you are not using a configuration set, comment or delete the
                    # following line
                    #ConfigurationSetName=CONFIGURATION_SET,
                )
            # Display an error if something goes wrong.	
                print("RN1",response)
            except ClientError as e:
                print(e.response['Error']['Message'])
                print("RN2",response)
            else:
                print("RN3",response)
                print("Email sent! Message ID:"),
                print(response['MessageId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }
