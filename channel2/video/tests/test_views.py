from django.urls.base import reverse

from channel2.base.tests import BaseTestCase


class IndexViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('index')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/index.html')
