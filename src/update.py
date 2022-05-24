"""Code related with the update"""
import json
import logging
import src.decimalencoder
import src.todoList


def update(event, context):
    """Provides the logic to update values."""
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
    # update the todo in the database
    result = src.todoList.update_item(
        event['pathParameters']['id'],
        data['text'], data['checked'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=src.decimalencoder.DecimalEncoder)
    }

    return response
