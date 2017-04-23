import os
from collections import namedtuple

from django.conf import settings
from django.http.response import HttpResponseBadRequest, Http404
from django.urls.base import reverse

from channel2.base.views import ProtectedTemplateView

# A tuple that holds the properties of a file for rendering in templates.
FileInfo = namedtuple('FileInfo', ['name', 'url', 'size'])


class DirectoryView(ProtectedTemplateView):

    template_name = 'video/directory.html'

    def get(self, request, path):
        if os.path.normpath(path).startswith('..'):
            return HttpResponseBadRequest()
        return self.render_to_response({
            'files': self.get_files(path)
        })

    def get_files(self, path):
        dirpath = os.path.join(settings.MEDIA_ROOT, path)
        if not os.path.isdir(dirpath):
            raise Http404
        files = []
        for filename in os.listdir(dirpath):
            url_path = os.path.join(path, filename)
            file_info = FileInfo(
                filename,
                reverse('directory', args=[url_path]),
                os.path.getsize(os.path.join(dirpath, filename)))
            files.append(file_info)
        return files
