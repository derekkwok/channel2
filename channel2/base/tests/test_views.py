from unittest import mock

from channel2.base.tests import BaseTestCase
from channel2.base.views import static_view


class BaseViewTest(BaseTestCase):

    def create_request(self):
        request = mock.Mock()
        request.META = {}
        return request

    def test_static_view(self):
        request = self.create_request()
        response = static_view(request, 'css/channel2.css')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/css')
        self.assertTrue(response['Last-Modified'])
        self.assertTrue(response.content)

    def test_static_view_bad_request(self):
        request = self.create_request()
        response = static_view(request, 'css/../../manage.py')
        self.assertEqual(response.status_code, 400)

    def test_static_view_not_found(self):
        request = self.create_request()
        response = static_view(request, 'some/bad/path/file.txt')
        self.assertEqual(response.status_code, 404)

    def test_static_view_not_modified(self):
        request = self.create_request()
        response = static_view(request, 'css/channel2.css')
        request.META['HTTP_IF_MODIFIED_SINCE'] = response['Last-Modified']
        response = static_view(request, 'css/channel2.css')
        self.assertEqual(response.status_code, 304)
