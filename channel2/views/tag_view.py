from typing import Text

from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module
from django.shortcuts import get_object_or_404

from channel2.data.models import video_model
from channel2.data.models import tag_model
from channel2.lib import views, file_lib


class TagView(views.TemplateView):

    template_name = 'web/pages/tag.html'

    def get(self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del request  # Unused.
        tag = get_object_or_404(tag_model.Tag, pk=tag_pk)
        if tag.slug != tag_slug:
            return shortcuts.redirect('tag', tag_pk=tag_pk, tag_slug=tag.slug)
        return self.render_to_response({
            'tag': tag,
            'tag_children': tag.children.all().order_by('name'),
            'tag_parents': tag.parents.all().order_by('name'),
            'videos': video_model.Video.objects.filter(tag=tag).order_by('name'),
        })

    def post(
            self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del tag_slug  # Unused.
        tag = get_object_or_404(tag_model.Tag, pk=tag_pk)
        for file in request.FILES.getlist('files'):
            file_lib.create_video(file, tag)
        return shortcuts.redirect('tag', tag_pk=tag_pk, tag_slug=tag.slug)
