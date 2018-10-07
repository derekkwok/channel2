from django.http import request as req_module
from django.http import response as resp_module

from channel2.lib import views


class IndexView(views.TemplateView):

    template_name = 'web/index.html'

    def get(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        del request  # Unused.
        return self.render_to_response({})
