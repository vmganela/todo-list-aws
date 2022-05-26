"""Code related with the list call"""
import json
import decimalencoder
import todoList


def list(event, context):
    """logic for the list"""
    # fetch all todos from the database
    result = todoList.get_items()
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result, cls=decimalencoder.DecimalEncoder)
    }
    return response
