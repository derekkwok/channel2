from typing import Any, Dict, Text

from django.http import response
from django.views.generic import base

from channel2.lib import template_lib


class TemplateView(base.View):

    template_name: Text = ''

    def render_to_response(self, context: Dict[Text, Any]) -> response.HttpResponse:
        return template_lib.render_to_response(self.template_name, self.request, context)
