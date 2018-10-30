from unittest import mock

from django import test, urls

from channel2.apps.data.models import tag_model
from channel2.forms import tag_create_anime_form


class TagCreateViewAnimeTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('tag.create.anime')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create_anime.html')

    def test_post_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create_anime.html')

    @mock.patch.object(tag_create_anime_form, 'TagCreateAnimeForm', autospec=True)
    def test_post(self, mock_form_cls):
        tag = tag_model.Tag.objects.create(name='Test Tag')
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = tag
        mock_form_cls.return_value = mock_form

        response = self.client.post(self.url, data={'kitsu_id': 101})
        self.assertRedirects(response, urls.reverse('tag', args=[tag.pk, tag.slug]))
