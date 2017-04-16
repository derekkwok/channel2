import re

from django.conf import settings
from django.http.response import HttpResponse
from django.utils.module_loading import import_string
from django.views.generic.base import View

from channel2.base.template import TEMPLATE_ENV

# Module-level cache for template context processors.
_context_processors = None


def get_context_processors():
    global _context_processors
    if _context_processors is None:
        _context_processors = tuple(
            import_string(path) for path in settings.JINJA2_CONTEXT_PROCESSORS)
    return _context_processors


class TemplateView(View):

    template_name = None

    def render_to_response(self, context):
        template = TEMPLATE_ENV.get_template(self.template_name)
        for processor in get_context_processors():
            context.update(processor(self.request))
        content = template.render(**context)
        content = re.sub(r'>\s+<', '><', content.strip())
        response = HttpResponse(content=content)
        response.template_name = self.template_name
        return response
