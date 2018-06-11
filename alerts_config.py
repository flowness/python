import add_measurement_utils
import boto3
dynamo = boto3.client('dynamodb')

def getAlertsConfig(moduleSN):
    response = dynamo.get_item(TableName='AlertConfig', Key=add_measurement_utils.getKeyForGetItem(moduleSN))
    print("Response alerts config: " + str(response))
    if 'Item' in response:
        return response['Item']
    else:
        return None 
