"""Code related with the get call"""
import json
import decimalencoder # pylint: disable=E0401
import todoList # pylint: disable=E0401


def translate(event, context):
    """logic for the translate"""
    # create a response
    item = todoList.translated_item(event['pathParameters']['id'],event['pathParameters']['lang'])
    print("ITEM EN TRANSLATE:{}".format(item))
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
