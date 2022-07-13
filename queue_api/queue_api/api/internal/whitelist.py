from flask_restful import Resource

from .security_decorator import internal_security


class InternalWhitelist(Resource):

    @internal_security
    def get(self):
        return

    @internal_security
    def post(self):
        return

    @internal_security
    def delete(self):
        return
