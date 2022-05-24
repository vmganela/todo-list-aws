"""Code related with the create call"""
import json
import logging
import src.todoList


def create(event, context):
    """Provides the logic to create values."""
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation failed")
        raise Exception("Couldn't create the todo item.")
    item = src.todoList.put_item(data['text'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    return response
