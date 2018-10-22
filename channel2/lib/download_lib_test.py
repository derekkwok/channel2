import unittest
from unittest import mock

import requests

from channel2.lib import download_lib


class DownloadLibTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.get_mock = mock.patch.object(requests, 'get', autospec=True).start()
        self.addCleanup(mock.patch.stopall)

    def test_download_file(self):
        response = mock.Mock()
        response.content = mock.sentinel.bytes
        self.get_mock.return_value = response

        file_data = download_lib.download_file('some/path/to/a/file.png')
        self.assertEqual(file_data.extension, 'png')
        self.assertEqual(file_data.bytes, mock.sentinel.bytes)
