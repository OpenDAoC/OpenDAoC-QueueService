from hashlib import md5
from flask import request
from flask_restful import Resource

from queue_api.queue_api.db.models.account import Account
from queue_api.queue_api.db.models.queue import QueueEntries
from queue_api.queue_api.db.models.whitelist import WhitelistEntries
from queue_api.queue_api.db.database import db


class QueueJoin(Resource):
    def post(self):
        data = request.get_json()
        try:
            name = data['name']
            password = data['password'].encode('utf-8')
            hashed_password = "##" + md5(password).hexdigest()
            account = Account.query.filter_by(name=name, password=hashed_password).first()
            if account is None:
                return {'success': False, 'error': 'an account with this user/pass combination does not exist'}, 401
            if account.privlevel > 1:
                return {'success': True, 'queue_bypass': True}, 200
            if WhitelistEntries.query.filter_by(name=account.name).first():
                return {'success': False, 'whitelisted': True}, 304
            if QueueEntries.query.filter_by(name=account.name).first():
                return {'success': False, 'queued': True}, 304
            queue_ticket = QueueEntries(name=account.name)
            db.session.add(queue_ticket)
            db.session.commit()
        except KeyError as e:
            return {'success': False, 'error': str(e)}, 400
        return {'success': True, 'queued': True}, 200
