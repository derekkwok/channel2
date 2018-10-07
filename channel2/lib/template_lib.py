import re
from typing import Any, Dict, Text

from django import urls
from django.conf import settings
from django.http import request, response
from django.template import defaultfilters
from jinja2 import environment, loaders

_TEMPLATE_ENV = environment.Environment(
    loader=loaders.FileSystemLoader(settings.JINJA2_DIRS),
    auto_reload=settings.DEBUG,
    autoescape=True,
)
_TEMPLATE_ENV.globals.update(
    url=urls.reverse,
)
_TEMPLATE_ENV.filters.update(
    date=defaultfilters.date,
    filesizeformat=defaultfilters.filesizeformat,
)


def render_to_response(
        template_name: Text,
        http_request: request.HttpRequest,
        context: Dict[Text, Any],
) -> response.HttpResponse:
    """Renders a template with the given name and context."""
    template = _TEMPLATE_ENV.get_template(template_name)
    for processor in settings.JINJA2_CONTEXT_PROCESSORS:
        context.update(processor(http_request))
    content = template.render(**context)
    content = re.sub(r'>\s+<', '><', content.strip())
    http_response = response.HttpResponse(content=content)
    http_response.template_name = template_name
    return http_response
