import mimetypes

from django.conf import settings
from django.http.response import HttpResponse


class HttpResponseXAccel(HttpResponse):

    def __init__(self, url, name):
        super().__init__()
        self['Content-Disposition'] = 'inline; filename={}'.format(name)
        self['Content-Type'] = (
            mimetypes.guess_type(url)[0] or 'application/octet-stream')
        self['X-Accel-Redirect'] = url
        if settings.DEBUG:
            self['Location'] = url
            self.status_code = 302
