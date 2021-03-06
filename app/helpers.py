"""
This module implements helper functions used in web service.

@author: Rohit Chormale
"""


import json
import datetime
import uuid
from bson.objectid import ObjectId
from flask import flash


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


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
