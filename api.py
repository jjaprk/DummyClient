import requests


import pdb


def connect(url, user_id):
    payload = {'id': user_id,'password': 'popo'}
    files = []
    headers = {}
    response = requests.request("POST", url + '/API/auth/', headers=headers, data=payload, files=files)
    return response


def get_game_list(url, token):
    payload = {}
    files = {}
    headers = {'Authorization': 'Token ' + token}
    response = requests.request("POST", url + '/API/game/list/', headers=headers, data=payload, files=files)
    return response


def create_game(url, game_cost, token):
    payload = {'game_cost': str(game_cost) }
    files = []
    headers = {'Authorization': 'Token ' + token}
    response = requests.request("POST", url + '/API/game/create/', headers=headers, data=payload, files=files)
    return response


def resume_game(url, game_pk, token):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}
    response = requests.request("POST", url + '/API/game/join/', headers=headers, data=payload, files=files)
    return response


def insert_credit(url, game_pk, credit, token):
    payload = {'credit': str(credit), 'game_pk': game_pk}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/insert_credit/', headers=headers, data=payload, files=files)
    return response


def spend_coin(url, game_pk, token):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/spend_coin/', headers=headers, data=payload, files=files)
    return response


def coin_result(url, game_pk, result, token):
    payload = {'game_pk': str(game_pk), 'result': result}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/coin_result/', headers=headers, data=payload, files=files)
    return response


def begin_spin(url, game_pk, token):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/begin_spin/', headers=headers, data=payload, files=files)
    return response


def end_spin(url, game_pk, token ):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/end_spin/', headers=headers, data=payload, files=files)
    return response


def gift_to_point(url, game_pk, token):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/gift_to_coin/', headers=headers, data=payload, files=files)
    return response


def close_game(url, game_pk, token):
    payload = {'game_pk': str(game_pk)}
    files = []
    headers = {'Authorization': 'Token ' + token}

    response = requests.request("POST", url + '/API/game/close/', headers=headers, data=payload, files=files)
    return response
