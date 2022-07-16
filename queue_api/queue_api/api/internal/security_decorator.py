from functools import wraps
from flask import request
from flask_restful import abort

from queue_api.queue_api.credentials import QUEUE_INTERNAL_SECRET


def internal_security(f):
    @wraps(f)
    def check_authorization(*args, **kwargs):
        if request.headers.get("Authorization") == QUEUE_INTERNAL_SECRET:
            return f(*args, **kwargs)
        else:
            return abort(401)
    return check_authorization
