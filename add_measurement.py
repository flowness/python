from __future__ import print_function
from uuid import uuid4
import alerts_config
import boto3
import json
import add_measurement_utils

print('Loading function')
dynamo = boto3.client('dynamodb')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    err = validateEvent(event)
    checkAlertsAndNotify(event)
    if not err:
        return respond(None, dynamo.put_item(TableName='Measurement',Item=getItem(event)))
    else:
        return respond(err)

def checkAlertsAndNotify(event):
    alertsConfig = alerts_config.getAlertsConfig(event['moduleSN'])
    if alertsConfig is None:
        return
    print ("alerts config:" + str(alertsConfig))
    zeroFlowHoursAlert = alertsConfig['zeroFlowHoursAlert']['BOOL']
    print("zeroFlowHoursAlert = " + str(zeroFlowHoursAlert))
    if zeroFlowHoursAlert:
        zeroFlowHoursStart = alertsConfig['zeroFlowHoursStart']['S']
        print("zeroFlowHoursStart = " + zeroFlowHoursStart)
        if add_measurement_utils.timeCompareToCurrent(zeroFlowHoursStart, True):
            zeroFlowHoursEnd = alertsConfig['zeroFlowHoursEnd']['S']
            print("zeroFlowHoursEnd = " + zeroFlowHoursEnd)
            if add_measurement_utils.timeCompareToCurrent(zeroFlowHoursEnd, False):
                x = {
                     'title': 'Lior',
                     'body': 'The King',
                     'moduleSN': event['moduleSN'],
                     'notificationType': 1
                    }
                invoke_response = lambda_client.invoke(FunctionName="sendToFCM", InvocationType='Event', Payload=json.dumps(x))
                print ("invoke response" + invoke_response['Payload'].read().decode())

def validateEvent(event):
    argsList = ['moduleSN', 'measurementDate', 'measurementAmount', 'measurementInterval','totalCount']
    for arg in argsList:
        if not arg in event:
            return ValueError('The body is missing a parameter: {}'.format(arg))
    if not isModuleExists(event):
        return ValueError('Module with this S/N does not exists')
        
def isModuleExists(event):
    response = dynamo.query(TableName='Module',IndexName='moduleSN-index',KeyConditions=getModuleBySNCondition(event))
    print("Response: " + str(response))
    return response['Count'] > 0

def getModuleBySNCondition(event):
    key_dict = {
        'moduleSN': {
            'AttributeValueList': [
                {'S':event['moduleSN']}
            ],
            'ComparisonOperator': 'EQ'
        }
    }
    # print ("key_str: " + str(key_str))
    return key_dict

def getItem(event):
    item_str = {
        'measurementId': {'S':str(uuid4())},
        'moduleSN': {'S':event['moduleSN']},
        'measurementDate': {'S':event['measurementDate']},
        'measurementInterval': {'N':str(event['measurementInterval'])},
        'measurementAmount': {'N':str(event['measurementAmount'])},
        'totalCount': {'N':str(event['totalCount'])}
    }
    return item_str

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


