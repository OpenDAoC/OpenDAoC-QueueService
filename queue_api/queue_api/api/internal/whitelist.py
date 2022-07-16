import traceback

from flask import request
from flask_restful import Resource
from sqlalchemy import delete

from .security_decorator import internal_security
from ...db.database import db
from ...db.models.queue import QueueEntries


class InternalWhitelist(Resource):
    decorators = [internal_security]

    def get(self):
        try:
            whitelisted_users = QueueEntries.query.filter_by(whitelisted=True).all()
            users = [{"name": x.name, "date_revoke": x.date_revoke.isoformat() if x.date_revoke else None} for x in whitelisted_users]
        except Exception as e:
            return {'success': False, 'error': str(traceback.format_exc())}, 500
        return {'success': True, 'users': users}, 200

    def post(self):
        try:
            body = request.get_json()
            name = body["name"]
            queue_ticket = QueueEntries.query.filter_by(name=name).first()
            if not queue_ticket:
                return {'success': False, 'message': 'user is not in queue', 'queued': False}, 400
            QueueEntries.query.filter_by(name=name).update({"whitelisted": True})
            db.session.commit()
        except Exception as e:
            return {'success': False, 'error': str(traceback.format_exc())}, 500
        return {'success': True, 'message': 'user was removed from queue and added to whitelist'}, 200

    def put(self):
        data = request.get_json()
        try:
            users = data["users"]
            graceful = data["graceful"]
            if graceful:
                for user in users:
                    queue_ticket = QueueEntries.query.filter_by(name=user).first()
                    if not queue_ticket:
                        continue
                    QueueEntries.query.filter_by(name=user).update({"date_revoke": None})
            else:
                for user in users:
                    queue_ticket = QueueEntries.query.filter_by(name=user["name"]).first()
                    if not queue_ticket:
                        continue
                    QueueEntries.query.filter_by(name=user["name"]).update({"date_revoke": user["date_revoke"]})
            db.session.commit()
        except Exception as e:
            return {'success': False, 'error': str(traceback.format_exc())}, 500
        return {'success': True, 'message': 'user(s) had a revocation date applied'}, 200

    def delete(self):
        data = request.get_json()
        try:
            users = data["users"]
            sql = delete(QueueEntries).where(QueueEntries.name.in_(users))
            db.session.execute(sql)
            db.session.commit()
        except Exception as e:
            return {'success': False, 'error': str(traceback.format_exc())}, 500
        return {'success': True, 'message': 'user(s) removed from whitelist'}, 200
