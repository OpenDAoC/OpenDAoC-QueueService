import atexit
from enum import Enum

import requests as requests
from apscheduler.schedulers.background import BackgroundScheduler
from credentials import *

api_urls = {
    "game_server_clients": f"https://api.atlasfreeshard.com/utils/query_clients/{GAME_SERVER_SECRET}",
    "queue": f"http://{QUEUE_API_HOST}/api/v1/internal/queue",
    "whitelist": f"http://{QUEUE_API_HOST}/api/v1/internal/whitelist"
}


# this enum is pointless unless we are going to track charscreen count & boot AFK
class playerState(Enum):
    connecting = 1
    charscreen = 2
    worldenter = 3
    playing = 4
    linkdead = 5
    disconnected = 6


def secure_headers():
    return {"Authorization": QUEUE_INTERNAL_SECRET}


# Get dictionary of all connected clients from game server (account_name : client_details)
def get_current_clients():
    r = requests.get(url=api_urls["game_server_clients"])
    return r.json()


# Get list of size @length of accounts at the front of the queue
def get_queue(length: int):
    params = {
        "length": length
    }
    r = requests.get(url=api_urls["queue"], params=params, headers=secure_headers())
    return r.json()


# retrieve the whole whitelist
def get_whitelist():
    r = requests.get(url=api_urls["whitelist"], headers=secure_headers())
    return r.json()


# add an account to the whitelist
def add_to_whitelist(account: str):
    data = {
        "name": account
    }
    r = requests.post(url=api_urls["whitelist"], data=data, headers=secure_headers())
    return r.json()


# remove an account from the whitelist
def remove_from_whitelist(account: str):
    data = {
        "name": account
    }
    r = requests.delete(url=api_urls["whitelist"], data=data, headers=secure_headers())
    return r.json()


def process_queue():

    clients = get_current_clients()
    total_states = {
        "connecting": 0,
        "charscreen": 0,
        "worldenter": 0,
        "playing": 0,
        "linkdead": 0,
        "disconnected": 0
    }

    total_team = 0
    for k, v in clients.items():
        print(k, v)
        if v['privLevel'] == 2 or v['privLevel'] == 3:
            total_team += 1
            del clients[k]
            continue
        if v["state"] == 1:
            total_states['connecting'] += 1
        elif v["state"] == 2:
            total_states['charscreen'] += 1
        elif v["state"] == 3:
            total_states['worldenter'] += 1
        elif v["state"] == 4:
            total_states['playing'] += 1
        elif v["state"] == 5:
            total_states['linkdead'] += 1
        elif v["state"] == 6:
            total_states['disconnected'] += 1

    total_clients = len(clients.keys())
    player_count = total_clients - total_team
    print('total clients:', total_clients)
    print('total team clients:', total_team)
    print('total player clients:', player_count)
    print('current player cap:', MAX_PLAYERS)
    print('open slots: ', MAX_PLAYERS - player_count)
    print('client state breakdown:', total_states)
    return


def shutdown():
    return


sched = BackgroundScheduler(daemon=True)
sched.add_job(process_queue, 'interval', seconds=30)
sched.start()
atexit.register(lambda: shutdown)

if __name__ == "__main__":
    process_queue()
