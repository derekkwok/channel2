import os

from django.conf import settings
from django.urls.base import reverse

from channel2.base.tests import BaseTestCase


class TempFile:

    def __init__(self, path, content):
        self.path = os.path.join(settings.MEDIA_ROOT, 'current', path)
        self.content = content

    def __enter__(self):
        with open(self.path, 'w') as f:
            f.write(self.content)

    def __exit__(self, *args):
        if os.path.exists(self.path):
            os.remove(self.path)


class DirectoryViewTest(BaseTestCase):

    def get_url(self, path='current'):
        return reverse('directory', args=[path])

    def test_get_anonymous(self):
        self.client.logout()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response,
            '{}?next={}'.format(reverse('account:login'), self.get_url()))

    def test_get(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/directory.html')

    def test_get_bad_path1(self):
        response = self.client.get(self.get_url('..'))
        self.assertEqual(response.status_code, 400)

    def test_get_bad_path2(self):
        response = self.client.get(self.get_url('../'))
        self.assertEqual(response.status_code, 400)

    def test_get_not_found(self):
        response = self.client.get(self.get_url('bad_path'))
        self.assertEqual(response.status_code, 404)

    def test_get_not_directory(self):
        response = self.client.get(self.get_url('current/file1.mp4'))
        self.assertEqual(response.status_code, 404)
