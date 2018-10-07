from unittest import mock

from django import test

from channel2.lib import template_lib, views

class TestView(views.TemplateView):
    """View class that extends TemplateView used for testing."""

    template_name = 'test/test-template.html'


class TemplateViewTest(test.TestCase):

    @mock.patch.object(template_lib, 'render_to_response', autospec=True)
    def test_render_to_response(self, mock_render):
        view = TestView(request=mock.sentinel.request)
        view.render_to_response(mock.sentinel.context)
        mock_render.assert_called_once_with(
            'test/test-template.html', mock.sentinel.request, mock.sentinel.context)
