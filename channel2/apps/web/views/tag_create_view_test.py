from django import test, urls


class TagCreateViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('tag.create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create.html')
