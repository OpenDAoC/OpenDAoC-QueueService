from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

from queue_api.queue_api.api.internal.queue import InternalQueue
from queue_api.queue_api.api.internal.whitelist import InternalWhitelist
from .public.queue.join import QueueJoin
from .public.queue.queue import PublicQueue
from .public.whitelist.whitelist import PublicWhitelist

v1 = Blueprint("v1", __name__)
CORS(v1)

api = Api()
api.init_app(v1)


@v1.route("/")
def health_check():
    return "atlas-queue-service-api-v1"


api.add_resource(PublicQueue, "/queue")
api.add_resource(QueueJoin, "/queue/join")
api.add_resource(PublicWhitelist, "/whitelist/check")

api.add_resource(InternalQueue, "/internal/queue")
api.add_resource(InternalWhitelist, "/internal/whitelist")
