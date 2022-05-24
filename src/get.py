"""Code related with the get call"""
import json
import src.decimalencoder
import src.todoList


def get(event, context):
    """logic for the get"""
    # create a response
    item = src.todoList.get_item(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=src.decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
