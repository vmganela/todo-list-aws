"""Workaround for: http://bugs.python.org/issue16535"""
import decimal
import json


# This is a workaround for: http://bugs.python.org/issue16535
class DecimalEncoder(json.JSONEncoder):
    """Defaul function DecimalEncoder"""
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
