import os

QUEUE_DB_NAME = os.environ.get('QUEUE_DB_NAME', 'queue')
QUEUE_DB_USER = os.environ.get('QUEUE_DB_USER', 'queue')
QUEUE_DB_PASS = os.environ.get('QUEUE_DB_PASS', 'queue')
QUEUE_DB_HOST = os.environ.get('QUEUE_DB_HOST', '127.0.0.1')
QUEUE_DB_PORT = os.environ.get('QUEUE_DB_PORT', '3306')

ATLAS_DB_NAME = os.environ.get('ATLAS_DB_NAME', 'atlas')
ATLAS_DB_USER = os.environ.get('ATLAS_DB_USER', 'atlas')
ATLAS_DB_PASS = os.environ.get('ATLAS_DB_PASS', 'atlas')
ATLAS_DB_HOST = os.environ.get('ATLAS_DB_HOST', '127.0.0.1')
ATLAS_DB_PORT = os.environ.get('ATLAS_DB_PORT', '3306')

QUEUE_INTERNAL_SECRET = os.environ.get('QUEUE_INTERNAL_SECRET', 'secret_alb_hib_love_affair')
GAME_SERVER_SECRET = os.environ.get('GAME_SERVER_SECRET', 'no_bread_for_you')