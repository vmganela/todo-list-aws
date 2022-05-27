"""Code related with the get call"""
import json
import decimalencoder # pylint: disable=E0401
import todoList # pylint: disable=E0401


def get(event, context):
    """logic for the get"""
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
