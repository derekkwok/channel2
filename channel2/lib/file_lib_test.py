import os
import tempfile

from django import test
from django.core.files import uploadedfile
from django.test import override_settings

from channel2.data.models import tag_model
from channel2.lib import file_lib


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class FileLibTest(test.TestCase):

    def test_create_video(self):
        file = uploadedfile.SimpleUploadedFile('file1.mp4', b'Hello World!')
        tag = tag_model.Tag.objects.create(name='Test Tag')
        video = file_lib.create_video(file, tag)
        self.assertEqual(video.name, 'file1.mp4')
        self.assertEqual(video.file.name, os.path.join('video', 'Test Tag', 'file1.mp4'))
        self.assertEqual(video.file.read(), b'Hello World!')  # pylint: disable=no-member
