from django import test
from django.db.models import deletion

from channel2.data.models import video_model
from channel2.data.models import tag_model


class VideoTest(test.TestCase):

    def test_save_without_file(self):
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
