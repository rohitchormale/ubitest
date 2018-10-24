"""
This module implements helper functions used in web service.

@author: Rohit Chormale
"""


import json
import datetime
import uuid
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    """Encode datetime object and mongo object-id as string"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def generate_transaction_id():
    return str(uuid.uuid4())

