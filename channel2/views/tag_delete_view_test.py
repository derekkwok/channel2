from django import test, urls

from channel2.data.models import tag_model


class TagDeleteViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.tag = tag_model.Tag.objects.create(name='Test Tag')
        self.url = urls.reverse('tag.delete', args=[self.tag.pk, self.tag.slug])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post_404(self):
        response = self.client.post(urls.reverse('tag.delete', args=[0, 'invalid-tag']))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, urls.reverse('index'))
        self.assertFalse(tag_model.Tag.objects.filter(name='Test Tag').exists())
