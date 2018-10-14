from django import test, urls

from channel2.apps.data.models import tag as tag_module


class TagCreateViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('tag.create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create.html')

    def test_post_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create.html')

    def test_post(self):
        response = self.client.post(self.url, data={
            'name': 'New Tag',
            'type': tag_module.TagType.ANIME
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
