"""Code related with the list call"""
import json
import src.decimalencoder
import src.todoList


def list(event, context):
    """logic for the list"""
    # fetch all todos from the database
    result = src.todoList.get_items()
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result, cls=src.decimalencoder.DecimalEncoder)
    }
    return response
