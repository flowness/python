from __future__ import print_function
import json
import boto3
import get_alerts_utils

dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    print ("res"+ str(res))
    print ("json res"+ json.dumps(res))
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    alerts = getAlertsConfig(event)
    return respond(None, alerts)

def getAlertsConfig(event):
    moduleSN = get_alerts_utils.getValueFromEvent(event, 'moduleSN', '')

    response = dynamo.get_item(TableName='AlertConfig', Key=get_alerts_utils.getKeyForGetItem(moduleSN))
    print("Response alerts config: " + str(response))
    return response['Item']
