"""Code related with the delete call"""
import src.todoList


def delete(event, context):
    """Provides the logic to delete values."""
    src.todoList.delete_item(event['pathParameters']['id'])

    # create a response
    response = {
        "statusCode": 200
    }

    return response
