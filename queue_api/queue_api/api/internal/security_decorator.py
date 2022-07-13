from functools import wraps

from flask import request

from queue_api.queue_api.credentials import QUEUE_INTERNAL_SECRET


def internal_security(f):
    @wraps(f)
    def check_authorization(*args, **kwargs):
        if request.headers.get("Authorization") == QUEUE_INTERNAL_SECRET:
            return f()
        else:
            return "lol"
    return check_authorization
