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

print(GAME_SERVER_API_HOST)
print(QUEUE_API_HOST, flush=True)


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
    data = {
        "length": length
    }
    r = requests.post(url=api_urls["queue"], json=data, headers=secure_headers())
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
    r = requests.post(url=api_urls["whitelist"], json=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# add revocation date to a list of accounts from the whitelist
def add_revoke_date_to_whitelist(revoke_list: list):
    data = {
        "users": revoke_list,
        "graceful": False
    }
    r = requests.put(url=api_urls["whitelist"], json=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# remove revocation date from a list of accounts from the whitelist
def remove_revoke_date_from_whitelist(grace_list: list):
    data = {
        "users": grace_list,
        "graceful": True
    }
    r = requests.put(url=api_urls["whitelist"], json=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


# remove an account from the whitelist
def remove_from_whitelist(account_list: list):
    data = {
        "users": account_list
    }
    r = requests.delete(url=api_urls["whitelist"], json=data, headers=secure_headers())
    if r.status_code != 200:
        return r.text, r.status_code
    return r.json(), r.status_code


def process_queue():
    clients, status_code = get_current_clients()
    if status_code != 200:
        print('get_current_clients', clients, status_code, flush=True)
        return

    total_team = 0
    for k in list(clients.keys()):
        client = clients[k]
        if client['privLevel'] == 2 or client['privLevel'] == 3:
            total_team += 1
            del clients[k]
            continue
        if client["state"] == 6:  # disconnected
            del clients[k]

    total_clients = len(clients.keys())
    player_count = total_clients - total_team
    available_slots = MAX_PLAYERS - player_count

    request_whitelisted_players, status = get_whitelist()
    if status != 200:
        print('get_whitelist', status_code, request_whitelisted_players, flush=True)
        return
    whitelisted_players = request_whitelisted_players['users']

    date_now = datetime.now()
    revoke_time = date_now + timedelta(minutes=1)
    connected_client_name_list = clients.keys()

    accounts_reconnected_during_grace = []
    accounts_need_revoke_date = []
    accounts_to_revoke = []

    for x in whitelisted_players:
        if x["name"] not in connected_client_name_list:
            if x.get('date_revoke', None) is None:
                accounts_need_revoke_date.append({
                    "name": x["name"],
                    "date_revoke": revoke_time.isoformat()
                })
            else:
                user_revoke_date = parser.parse(x["date_revoke"])
                if date_now >= user_revoke_date:
                    accounts_to_revoke.append(x["name"])
        elif x["date_revoke"] is not None and x["name"] in connected_client_name_list:
            accounts_reconnected_during_grace.append(x["name"])

    removed_revoke_date, status_code = remove_revoke_date_from_whitelist(accounts_reconnected_during_grace)
    if status_code != 200:
        print('remove_revoke_date_to_whitelist', status_code, removed_revoke_date, flush=True)
        return

    applied_revoke_date, status_code = add_revoke_date_to_whitelist(accounts_need_revoke_date)
    if status_code != 200:
        print('add_revoke_date_to_whitelist', status_code, applied_revoke_date, flush=True)
        return

    revoked_accounts, status_code = remove_from_whitelist(accounts_to_revoke)
    if status_code != 200:
        print('remove_from_whitelist', status_code, revoked_accounts, flush=True)
        return

    players_next_in_line, status_code = get_queue(available_slots)
    if status_code != 200:
        print('get_queue', status_code, players_next_in_line, flush=True)
        return

    successfully_whitelisted_count = 0
    for player in players_next_in_line:
        res, status_code = add_to_whitelist(player["name"])
        if status_code != 200:
            print('add_to_whitelist: ', player["name"], status_code, res)
        else:
            successfully_whitelisted_count += 1

    print('total clients:', total_clients)
    print('total team clients:', total_team)
    print('total player clients:', player_count)
    print('current player cap:', MAX_PLAYERS)
    print('open slots: ', available_slots)
    print(f'whitelisted {successfully_whitelisted_count} users from: ', players_next_in_line)
    print('accounts given grace: ', accounts_reconnected_during_grace)
    print('accounts primed to revoke: ', accounts_need_revoke_date)
    print('revoked accounts: ', accounts_to_revoke)
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