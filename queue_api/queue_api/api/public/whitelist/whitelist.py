from flask import request
from flask_restful import Resource
from sqlalchemy import and_

from queue_api.queue_api.db.database import db
from queue_api.queue_api.db.models.queue import QueueEntries


class PublicWhitelist(Resource):
    def post(self):
        try:
            data = request.get_json() or request.form
            name = data.get("name")
            query = db.session.query(QueueEntries).filter(
                and_(
                    QueueEntries.name == name,
                    QueueEntries.whitelisted.is_(True)
                )
            ).first()
            status_code = 200 if query is not None else 404
        except Exception as e:
            return {'success': False, 'position': -1, 'error': str(e)}, 500
        return {'success': True}, status_code
