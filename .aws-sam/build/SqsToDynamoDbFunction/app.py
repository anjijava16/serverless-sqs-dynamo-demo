import logging
from json import loads

import boto3

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s'
)

logging.info('Loading function')

dynamo_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    for record in event['Records']:
        payload = loads(record['body'], parse_float=str)
        operation = record['messageAttributes']['Method']['stringValue']
        if operation in operations:
            operations[operation](dynamo_client, payload)
            logging.info('{} successful'.format(operation))
        else:
            logging.error('Unsupported method \'{}\''.format(operation))