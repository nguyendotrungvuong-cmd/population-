import json

import requests


def fetch_data(API, URL, country):
    headers = {"X-Api-Key": API}
    params = {"country": country}
    respones = requests.get(URL, headers=headers, params=params)
    respones.raise_for_status()
    return respones.json()
