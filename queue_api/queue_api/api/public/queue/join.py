import json
from hashlib import md5
from flask import request
from flask_restful import Resource

from sqlalchemy import text

from queue_api.queue_api.api.public.queue.queue import get_queue_position_by_name
from queue_api.queue_api.db.atlas_database import atlas_session, ATLAS_DATABASE_URL
from queue_api.queue_api.db.models.queue import QueueEntries
from queue_api.queue_api.db.database import db, QUEUE_DATABASE_URL


class QueueJoin(Resource):

    # JOIN QUEUE
    def post(self):
        data = request.get_json()
        try:
            name = data['name']
            password = data['password']

            res = []
            for i in range(0, len(password)):
                res += chr(ord(password[i]) >> 8)
                res += chr(ord(password[i]))
            encoded_password_string = "".join(res).encode('utf-8')
            hashed = md5(encoded_password_string).hexdigest().upper()
            hash_len = len(hashed)
            for x in (reversed(range(0, hash_len - 1, 2))):
                if hashed[x] == "0":
                    hashed = hashed[0:x] + hashed[x+1:hash_len]

            hashed_password = "##" + hashed
            game_server_session = atlas_session()
            payload = {"name": name, "password": hashed_password}
            query = text("""SELECT name, privlevel FROM account WHERE name=:name AND password=:password""")
            res = game_server_session.execute(query, payload)
            account = res.first()

            # account = Account.query.filter_by(name=name, password=hashed_password).first()
            if account is None:
                return {'success': False, 'error': 'an account with this user/pass combination does not exist'}, 401
            if account.privlevel > 1:
                return {'success': True, 'queue_bypass': True, 'queued': False, 'whitelisted': False}, 200
            if QueueEntries.query.filter_by(name=account.name, whitelisted=True).first():
                return {'success': True, 'queue_bypass': False, 'queued': False, 'whitelisted': True}, 200
            if QueueEntries.query.filter_by(name=account.name, whitelisted=False).first():
                return {'success': True, 'queue_bypass': False, 'queued': True, 'whitelisted': False}, 200
            queue_ticket = QueueEntries(name=account.name)
            db.session.add(queue_ticket)
            db.session.commit()

            position, status = get_queue_position_by_name(name)
            if status != 200:
                return position, status
        except Exception as e:
            return {'success': False, 'error': str(e), "queue_db_uri": QUEUE_DATABASE_URL, "atlas_db_uri": ATLAS_DATABASE_URL}, 400
        return {'success': True, 'queued': True, 'position': position}, 200
