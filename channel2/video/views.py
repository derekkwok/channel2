import os
from collections import namedtuple

from django.conf import settings
from django.http.response import HttpResponseBadRequest, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic.base import View

from channel2.base.responses import HttpResponseXAccel
from channel2.base.views import ProtectedTemplateView
from channel2.video.models import VideoLink

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
            urlpath = os.path.join(path, filename).replace(os.sep, '/')
            filepath = os.path.join(dirpath, filename)
            file_info = FileInfo(
                filename, self.get_filename_url(filepath, urlpath),
                os.path.getsize(filepath))
            files.append(file_info)
        return files

    def get_filename_url(self, filepath, url_path):
        if os.path.isfile(filepath):
            return reverse('video:file', args=[url_path])
        elif os.path.isdir(filepath):
            return reverse('directory', args=[url_path])
        else:
            raise RuntimeError('Not file or directory: {}'.format(url_path))


class FileView(ProtectedTemplateView):

    def get(self, request, path):
        path = os.path.join(settings.MEDIA_URL, path)
        try:
            link = VideoLink.objects.filter(
                user=request.user, file_path=path,
                expires_on__gt=timezone.now()).latest('expires_on')
        except VideoLink.DoesNotExist:
            link = VideoLink.create(request.user, path)
        filename = os.path.basename(path)
        return redirect('video:link', link.link_path, filename)


class LinkView(View):

    def get(self, request, path, name):
        link = get_object_or_404(VideoLink, link_path=path)
        return HttpResponseXAccel(link.file_path, name)
