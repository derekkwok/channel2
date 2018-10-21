from django import test, urls

from channel2.apps.data.models import tag_model


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
