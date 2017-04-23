import os

from django.conf import settings
from django.urls.base import reverse

from channel2.base.tests import BaseTestCase
from channel2.video.models import VideoLink
from channel2.video.views import FileInfo, FileType


class FileInfoTest(BaseTestCase):

    def test_file(self):
        file = FileInfo('current', 'file1.mp4')
        self.assertEqual(file.name, 'file1.mp4')
        self.assertEqual(file.size, 12)
        self.assertEqual(file.type, FileType.FILE)
        self.assertEqual(
            file.url, reverse('video:file', args=['current/file1.mp4']))

    def test_dir(self):
        dir = FileInfo('', 'current')
        self.assertEqual(dir.name, 'current')
        self.assertEqual(dir.type, FileType.DIR)
        self.assertEqual(dir.url, reverse('directory', args=['current']))


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


class FileViewTest(BaseTestCase):

    def test_get(self):
        file_path = os.path.join(settings.MEDIA_URL, 'current/file1.mp4')
        video_link_qs = VideoLink.objects.filter(
            file_path=file_path, user=self.user)
        self.assertEqual(0, video_link_qs.count())

        # First get creates the video link.
        url = reverse('video:file', args=['current/file1.mp4'])
        response = self.client.get(url)
        link = video_link_qs.latest('expires_on')
        self.assertRedirects(
            response, reverse('video:link', args=[link.link_path, 'file1.mp4']))

        # Second get re-uses that video link.
        response = self.client.get(url)
        self.assertEqual(1, video_link_qs.count())
        self.assertRedirects(
            response, reverse('video:link', args=[link.link_path, 'file1.mp4']))


class LinkViewTest(BaseTestCase):

    def test_get(self):
        file_path = os.path.join(settings.MEDIA_URL, 'current/file.mp4')
        link = VideoLink.create(self.user, file_path)
        url = reverse('video:link', args=[link.link_path, 'file1.mp4'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'video/mp4')
        self.assertEqual(response['X-Accel-Redirect'], file_path)
