from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import text

from queue_api.queue_api.db.database import db
from queue_api.queue_api.db.models.queue import QueueEntries


class PublicQueue(Resource):
    def get(self):
        data = request.get_json()
        try:
            account = data["account"]
            queue_ticket = QueueEntries.query.filter_by(name=account).first()
            if not queue_ticket:
                return {'success': False, 'message': 'account is not in queue', 'queued': False}, 400
            payload = {"create_data": queue_ticket.date_create}
            query = text("""SELECT COUNT(1) FROM tbl WHERE create_date <= :create_date""")
            result = db.engine.execute(query, **payload)
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        return {'success': True, 'position': result}, 200

    def post(self):
        return
