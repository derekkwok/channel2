from unittest import mock

import requests
from django import test

from channel2.apps.data.gateways import kitsu_gateway


def _create_response(data):
    response = mock.Mock()
    response.json.return_value = data
    return response


class KitsuGatewayTest(test.TestCase):

    def setUp(self):
        self.get_mock = mock.patch.object(requests, 'get', autospec=True).start()
        self.addCleanup(mock.patch.stopall)

    def test_get_anime_data(self):
        self.get_mock.return_value = _create_response({'data': mock.sentinel.data})
        kitsu_id = 101
        data = kitsu_gateway.get_anime_data(kitsu_id)
        self.assertEqual(data, mock.sentinel.data)
        self.get_mock.assert_called_once_with('https://kitsu.io/api/edge/anime/101')

    def test_get_genre_data(self):
        self.get_mock.return_value = _create_response({'data': mock.sentinel.data})
        kitsu_id = 102
        data = kitsu_gateway.get_genre_data(kitsu_id)
        self.assertEqual(data, mock.sentinel.data)
        self.get_mock.assert_called_once_with('https://kitsu.io/api/edge/anime/102/genres')
