import os
import tempfile

from django import test
from django.conf import settings
from django.db.models import deletion
from django.test import override_settings

from channel2.data.models import tag_model
from channel2.data.models import video_model


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class VideoTest(test.TestCase):

    def test_video_save_without_file(self):
        with self.assertRaises(RuntimeError) as context_manager:
            video_model.Video.objects.create(name='Test video')
        self.assertEqual(context_manager.exception.args[0], 'The file attribute must be set.')

    def test_tag_delete_protect(self):
        tag = tag_model.Tag.objects.create(name='Test Tag')
        video_model.Video.objects.create(
            name='Test Video',
            file='some/arbitrary/path/to/video.mp4',
            tag=tag)
        with self.assertRaises(deletion.ProtectedError):
            tag.delete()

    def test_video_delete(self):
        with open(os.path.join(settings.MEDIA_ROOT, 'test.mp4'), 'w+') as file:
            file.write('Hello World!')
            file.close()

        tag = tag_model.Tag.objects.create(name='Test Tag')
        video = video_model.Video.objects.create(
            name='Test Video',
            file=file.name,
            tag=tag)
        self.assertTrue(os.path.exists(file.name))
        video.delete()
        self.assertFalse(os.path.exists(file.name))
