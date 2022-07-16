import traceback

from flask import request
from flask_restful import Resource
from sqlalchemy import text

from .security_decorator import internal_security
from ...db.database import db


class InternalQueue(Resource):
    decorators = [internal_security]

    def post(self):
        data = request.get_json()
        try:
            length = data["length"]
            payload = {"length": length}
            query = text(
                """SELECT name FROM queue_entries WHERE whitelisted IS NOT TRUE ORDER BY date_create LIMIT :length""")
            res = db.session.execute(query, payload)
        except Exception as e:
            return {"success": False, "error": str(traceback.format_exc())}
        return [dict(ix) for ix in res], 200
