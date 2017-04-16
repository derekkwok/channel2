from django.conf import settings
from django.urls.base import reverse

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


TEMPLATE_SETTINGS = {
    'loader': FileSystemLoader(settings.JINJA2_DIRS),
    'auto_reload': settings.DEBUG,
    'autoescape': True,
}
TEMPLATE_ENV = Environment(**TEMPLATE_SETTINGS)
TEMPLATE_ENV.globals.update(**{
    'url': reverse,
})
