from django import test, urls

from channel2.data.models import tag_model


class TagEditViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.tag = tag_model.Tag.objects.create(name='Test Tag')
        self.url = urls.reverse('tag.edit', args=[self.tag.pk, self.tag.slug])

    def test_get_404(self):
        response = self.client.get(urls.reverse('tag.edit', args=[0, 'invalid-tag']))
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_edit.html')

    def test_post_404(self):
        response = self.client.post(urls.reverse('tag.edit', args=[0, 'invalid-tag']))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post(self.url, data={
            'name': 'New Tag Name',
            'type': tag_model.TagType.ANIME_TAG,
        })
        tag = tag_model.Tag.objects.get(pk=self.tag.pk)
        self.assertEqual(tag.name, 'New Tag Name')
        self.assertEqual(tag.type, tag_model.TagType.ANIME_TAG)
        self.assertRedirects(response, urls.reverse('tag', args=[tag.pk, tag.slug]))
