import os
from collections import namedtuple

from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.urls.base import reverse

from channel2.base.views import ProtectedTemplateView

# A tuple that holds the properties of a file for rendering in templates.
FileInfo = namedtuple('FileInfo', ['name', 'url', 'size'])

# Character to replace %20 with in the URL. Allows for prettier URLs.
SPACE_CHAR = '+'


class IndexView(ProtectedTemplateView):
    """Lists files and directories."""

    template_name = 'video/index.html'

    def get(self, request, path=''):
        """Handles a GET request."""
        if os.path.normpath(path).startswith('..'):
            return HttpResponseBadRequest()
        return self.render_to_response({
            'files': self.get_files(path),
        })

    def get_files(self, path):
        """Gets a list of FileInfo objects for the given path."""
        path = path.replace(SPACE_CHAR, ' ')
        fullpath = os.path.join(settings.MEDIA_ROOT, path)
        files = []
        for filename in os.listdir(fullpath):
            filepath = os.path.join(path, filename).replace(' ', SPACE_CHAR)
            file_info = FileInfo(
                filename, reverse('video:index', args=[filepath]),
                os.path.getsize(os.path.join(fullpath, filename)))
            files.append(file_info)
        return files
