"""Code related with the update"""
import json
import logging
import decimalencoder # pylint: disable=E0401
import todoList # pylint: disable=E0401


def update(event, context):
    """Provides the logic to update values."""
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
    # update the todo in the database
    result = todoList.update_item(
        event['pathParameters']['id'],
        data['text'], data['checked'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
