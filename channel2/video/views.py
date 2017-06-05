import os
from collections import namedtuple
from datetime import datetime

from django.conf import settings
from django.http.response import HttpResponseBadRequest, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic.base import View

from channel2.base.responses import HttpResponseXAccel
from channel2.base.views import ProtectedTemplateView
from channel2.video.models import VideoLink

Breadcrumb = namedtuple('Breadcrumb', ['name', 'path'])


class FileType:

    DIR = 'dir'
    FILE = 'file'


class FileInfo:

    def __init__(self, path, filename):
        self.name = filename
        # Absolute filesystem path to the file.
        filepath = os.path.join(settings.MEDIA_ROOT, path, filename)
        self.mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        self.size = os.path.getsize(filepath)
        self.type = self.get_type(filepath)
        self.url = self.get_url(path, filename)

    def get_type(self, filepath):
        if os.path.isfile(filepath):
            return FileType.FILE
        elif os.path.isdir(filepath):
            return FileType.DIR
        else:
            raise RuntimeError('Not file or directory: {}'.format(filepath))

    def get_url(self, path, filename):
        url_path = os.path.join(path, filename).replace(os.sep, '/')
        if self.type == FileType.FILE:
            return reverse('video:file', args=[url_path])
        elif self.type == FileType.DIR:
            return reverse('directory', args=[url_path])
        else:
            raise RuntimeError('Unhandled type: {}'.format(self.type))


class DirectoryView(ProtectedTemplateView):

    template_name = 'video/directory.html'

    def get(self, request, path=''):
        if os.path.normpath(path).startswith('..'):
            return HttpResponseBadRequest()

        # If the current requested path is not a directory, return 404.
        dirpath = os.path.join(settings.MEDIA_ROOT, path)
        if not os.path.isdir(dirpath):
            raise Http404

        file_list = [
            FileInfo(path, filename) for filename in os.listdir(dirpath)]
        # Split files into files and directories.
        dirs = [file for file in file_list if file.type == FileType.DIR]
        files = [file for file in file_list if file.type == FileType.FILE]
        return self.render_to_response({
            'breadcrumbs': self.get_breadcrumbs(path),
            'dirs': dirs,
            'files': files,
        })

    def get_breadcrumbs(self, path):
        breadcrumbs = [Breadcrumb('Channel 2', '')]
        parts = path.split('/')
        for i in range(len(parts)):
            breadcrumbs.append(Breadcrumb(parts[i], '/'.join(parts[:i + 1])))
        return breadcrumbs


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
