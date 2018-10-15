from django import test, urls


class TagListViewTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('tag.list.anime')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_list.html')
