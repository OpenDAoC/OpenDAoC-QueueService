import os

QUEUE_API_HOST = os.environ.get('QUEUE_API_HOST', 'http://127.0.0.1:5000/')
QUEUE_INTERNAL_SECRET = os.environ.get('QUEUE_INTERNAL_SECRET', 'secret_alb_hib_love_affair')
GAME_SERVER_SECRET = os.environ.get('GAME_SERVER_SECRET', 'no_bread_for_you')
MAX_PLAYERS = int(os.environ.get('MAX_PLAYERS', 1375))