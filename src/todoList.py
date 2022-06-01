"""Main code of todo list applicacion"""

import os
import time
import uuid
import json
import functools
import boto3  # pylint: disable=E0401
from botocore.exceptions import ClientError


def get_table(dynamodb=None):
    """Restrieve the DB table"""
    try:
        if not dynamodb:
            dynamo_url = os.environ['ENDPOINT_OVERRIDE']
            if dynamo_url:
                print('URL dynamoDB:'+dynamo_url)
                boto3.client = functools.partial(boto3.client,
                                                 endpoint_url=dynamo_url)
                boto3.resource = functools.partial(boto3.resource,
                                                   endpoint_url=dynamo_url)
            dynamodb = boto3.resource("dynamodb")
        # fetch todo from the database
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        return table
    except Exception as error:
        print(error)

def get_item(key, dynamodb=None):
    """returns the item with the id passed from the database"""
    table = get_table(dynamodb)
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )

    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        print('Result getItem:'+str(result))
        if 'Item' in result:
            return result['Item']
    return None
    

def translated_item(key, lang, dynamodb=None):
    """returns the item with the id passed from the database translated in a specific languaje"""
    
    table = get_table(dynamodb)
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )
        translated_result = translate.translate_text(Text=result['Item']["text"], SourceLanguageCode="auto", TargetLanguageCode=lang)
        result['Item']["text"] = translated_result.get('TranslatedText')
        
    except ClientError as error:
        print(error.response['Error']['Message'])
    except Exception as error:
        print(error)
    else:
        print('Result getItem:'+str(result))
        if 'Item' in result:
            return result['Item']
            
    return None


def get_items(dynamodb=None):
    """returns all items in the db"""
    table = get_table(dynamodb)
    # fetch todo from the database
    result = table.scan()
    return result['Items']


def put_item(text, dynamodb=None):
    """Adds new item in the db"""
    table = get_table(dynamodb)
    timestamp = str(time.time())
    print('Table name:' + table.name)
    item = {
        'id': str(uuid.uuid1()),
        'text': text,
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    try:
        # write the todo to the database
        table.put_item(Item=item)
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        return response


def update_item(key, text, checked, dynamodb=None):
    """Updates the values of an item"""
    table = get_table(dynamodb)
    timestamp = int(time.time() * 1000)
    # update the todo in the database
    try:
        result = table.update_item(
            Key={
                'id': key
            },
            ExpressionAttributeNames={
                '#todo_text': 'text',
            },
            ExpressionAttributeValues={
                ':text': text,
                ':checked': checked,
                ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        return result['Attributes']


def delete_item(key, dynamodb=None):
    """Deletes the item with the given ID"""
    table = get_table(dynamodb)
    # delete the todo from the database
    try:
        table.delete_item(
            Key={
                'id': key
            }
        )
    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        return


def create_todo_table(dynamodb):
    """Creates a db for testing purpose"""
    table_name = os.environ['DYNAMODB_TABLE']
    print('Creating Table with name:' + table_name)
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    if table.table_status != 'ACTIVE':
        raise AssertionError()

    return table
