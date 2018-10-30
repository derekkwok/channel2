from django import test, urls


class IndexViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('index')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/index.html')
