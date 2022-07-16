import traceback

from flask import request
from flask_restful import Resource
from sqlalchemy import text

from queue_api.queue_api.db.database import db
from queue_api.queue_api.db.models.queue import QueueEntries


class PublicQueue(Resource):
    def get(self):
        return {'success': True, 'queue_length': 0}, 200

    # GET QUEUE POSITION
    def post(self):
        data = request.get_json()
        try:
            name = data["name"]
            position, status = get_queue_position_by_name(name)
            if status != 200:
                return position, status
        except Exception as e:
            return {'success': False, 'position': -1, 'error': str(traceback.format_exc())}, 500
        return {'success': True, 'position': position}, 200


def get_queue_position_by_name(name):
    queue_ticket = QueueEntries.query.filter_by(name=name).first()
    if not queue_ticket:
        return {'success': False, 'error': 'user is not in queue', 'position': -1}, 404
    payload = {"date_create": queue_ticket.date_create.isoformat()}
    query = text("""SELECT COUNT(1) FROM queue_entries WHERE whitelisted IS NOT TRUE AND date_create <= :date_create""")
    result = db.engine.execute(query, **payload).first()
    position = result[0]
    return position, 200
