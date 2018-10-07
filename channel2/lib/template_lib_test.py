import unittest

from django.http import request

from channel2.lib import template_lib


class TemplateLibTest(unittest.TestCase):

    def test_render_to_response(self):
        template_name = 'test/test-template.html'
        http_request = request.HttpRequest()
        context = {'var1': 'test-variable-1'}
        http_response = template_lib.render_to_response(template_name, http_request, context)
        self.assertEqual(http_response.template_name, template_name)
        self.assertIn(b'<p>Hello World!</p>', http_response.content)
        self.assertIn(b'test-variable-1', http_response.content)
