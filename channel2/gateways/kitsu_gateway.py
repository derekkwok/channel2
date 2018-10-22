from typing import Dict, Text

import requests


def get_anime_data(kitsu_id: Text) -> Dict:
    response = requests.get('https://kitsu.io/api/edge/anime/{}'.format(kitsu_id)).json()
    return response['data']


def get_genre_data(kitsu_id: Text) -> Dict:
    response = requests.get('https://kitsu.io/api/edge/anime/{}/genres'.format(kitsu_id)).json()
    return response['data']
