from typing import Text

from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module
from django.shortcuts import get_object_or_404

from channel2.data.models import tag_model
from channel2.lib import views


class TagDeleteView(views.TemplateView):

    allowed_methods = ['post']

    def post(
            self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del request  # Unused.
        del tag_slug  # Unused.
        tag = get_object_or_404(tag_model.Tag, pk=tag_pk)
        if tag.children.exists() or tag.parents.exists():
            return shortcuts.redirect('tag', tag_pk=tag.pk, tag_slug=tag.slug)
        tag.delete()
        return shortcuts.redirect('index')
