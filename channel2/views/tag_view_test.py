import tempfile

from django import test, urls
from django.core.files import uploadedfile
from django.test import override_settings

from channel2.data.models import video_model
from channel2.data.models import tag_model


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TagViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.tag = tag_model.Tag.objects.create(name='Test Tag')
        self.url = urls.reverse('tag', args=[self.tag.pk, self.tag.slug])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag.html')

    def test_get_wrong_slug(self):
        url = urls.reverse('tag', args=[self.tag.pk, 'wrong-slug'])
        response = self.client.get(url)
        self.assertRedirects(response, self.url)

    def test_post(self):
        response = self.client.post(self.url, data={
            'files': [
                uploadedfile.SimpleUploadedFile('file1.mp4', b''),
                uploadedfile.SimpleUploadedFile('file2.mp4', b''),
            ],
        })
        self.assertRedirects(response, self.url)
        video_list = video_model.Video.objects.filter(tag=self.tag)
        self.assertCountEqual(['file1.mp4', 'file2.mp4'], [v.name for v in video_list])
