import json

from django import test, urls

DATA = {
    'attributes': {
        'canonicalTitle': 'Cowboy Bepop',
        'synopsis': '',
    },
}


class TagCreateViewAnimeTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.url = urls.reverse('tag.create.anime')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create_anime.html')

    def test_post(self):
        response = self.client.post(self.url, data={'metadata': json.dumps(DATA)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'web/pages/tag_create_anime.html')
