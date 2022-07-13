from hashlib import md5

from flask import request
from flask_restful import Resource


class QueueJoin(Resource):
    def post(self):
        data = request.get_json()
        try:
            name = data['name']
            password = data['password'].encode('utf-8')
            hashed_password = "##" + md5(password).hexdigest()
            account = Account.query.filter_by(name=name, password=hashed_password).first()
            if account is None:
                return jsonify(
                    {'success': False, 'error': 'an account with this user/pass combination does not exist'}), 401
            if account.privlevel > 1:
                return jsonify({'success': True, 'queue_bypass': True})
            if account.name in queue:
                return jsonify({'success': False, 'position': queue.index(account.name) + 1})
            queue.append(account.name)
            return jsonify({'success': True, 'position': len(queue)})
        except KeyError as e:
            return jsonify({'success': False, 'error': str(e)}), 400

        return
