import atexit
import parser
import time
from datetime import datetime, timedelta
from enum import Enum

import requests as requests
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil import parser

from credentials import *

api_urls = {
    "game_server_clients": f"{GAME_SERVER_API_HOST}/utils/query_clients/{GAME_SERVER_SECRET}",
    "queue": f"{QUEUE_API_HOST}/api/v1/internal/queue",
    "whitelist": f"{QUEUE_API_HOST}/api/v1/internal/whitelist"
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
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# Get list of size @length of accounts at the front of the queue
def get_queue(length: int):
    params = {
        "length": length
    }
    r = requests.get(url=api_urls["queue"], params=params, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# retrieve the whole whitelist
def get_whitelist():
    r = requests.get(url=api_urls["whitelist"], headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# add an account to the whitelist
def add_to_whitelist(account: str):
    data = {
        "name": account
    }
    r = requests.post(url=api_urls["whitelist"], data=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# remove an account from the whitelist
def remove_from_whitelist(account: str):
    data = {
        "name": account
    }
    r = requests.delete(url=api_urls["whitelist"], data=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


def process_queue():
    clients, status_code = get_current_clients()
    if status_code != 200:
        print('oh shit game server kill?', clients, status_code, flush=True)
        return

    total_states = {
        "connecting": 0,
        "charscreen": 0,
        "worldenter": 0,
        "playing": 0,
        "linkdead": 0,
        "disconnected": 0
    }

    total_team = 0
    for k in list(clients.keys()):
        client = clients[k]
        if client['privLevel'] == 2 or client['privLevel'] == 3:
            total_team += 1
            del clients[k]
            continue
        if client["state"] == 1:
            total_states['connecting'] += 1
        elif client["state"] == 2:
            total_states['charscreen'] += 1
        elif client["state"] == 3:
            total_states['worldenter'] += 1
        elif client["state"] == 4:
            total_states['playing'] += 1
        elif client["state"] == 5:
            total_states['linkdead'] += 1
        elif client["state"] == 6:
            total_states['disconnected'] += 1

    total_clients = len(clients.keys())
    player_count = total_clients - total_team
    print('total clients:', total_clients)
    print('total team clients:', total_team)
    print('total player clients:', player_count)
    print('current player cap:', MAX_PLAYERS)
    print('open slots: ', MAX_PLAYERS - player_count)
    print('client state breakdown:', total_states)
    print('sleeping for 10 seconds...', flush=True)
    return


sched = BackgroundScheduler()
sched.add_job(process_queue, 'interval', seconds=10)
sched.start()
atexit.register(lambda: sched.shutdown(wait=False))


def main():
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
