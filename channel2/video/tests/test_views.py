import os

from django.conf import settings
from django.urls.base import reverse

from channel2.base.tests import BaseTestCase
from channel2.video.views import IndexView


class TempFile:

    def __init__(self, path, content):
        self.path = os.path.join(settings.MEDIA_ROOT, path)
        self.content = content

    def __enter__(self):
        with open(self.path, 'w') as f:
            f.write(self.content)

    def __exit__(self, *args):
        if os.path.exists(self.path):
            os.remove(self.path)


class IndexViewTest(BaseTestCase):

    def get_url(self, path=''):
        return reverse('video:index', args=[path])

    def test_get_anonymous(self):
        self.client.logout()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response,
            '{}?next={}'.format(reverse('account:login'), self.get_url()))

    def test_get(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/index.html')

    def test_get_bad_path1(self):
        response = self.client.get(self.get_url('..'))
        self.assertEqual(response.status_code, 400)

    def test_get_bad_path2(self):
        response = self.client.get(self.get_url('../'))
        self.assertEqual(response.status_code, 400)

    def test_get_files_empty(self):
        view = IndexView()
        files = view.get_files('')
        self.assertEqual(len(files), 0)

    def test_get_files(self):
        view = IndexView()
        with TempFile('f 1.txt', 'Hello!'), TempFile('f2.txt', 'Something'):
            files = view.get_files('')
            self.assertEqual(len(files), 2)
            filename_to_file = {f.name: f for f in files}
            file1 = filename_to_file['f 1.txt']
            self.assertEqual(file1.size, 6)
            self.assertEqual(file1.url, '/video/list/f+1.txt')
            file2 = filename_to_file['f2.txt']
            self.assertEqual(file2.size, 9)
            self.assertEqual(file2.url, '/video/list/f2.txt')
