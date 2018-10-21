from typing import Text

from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module

from channel2.apps.data.models import tag_model
from channel2.lib import views


class TagView(views.TemplateView):

    template_name = 'web/pages/tag.html'

    def get(self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del request  # Unused.
        tag = tag_model.Tag.objects.get(pk=tag_pk)
        if tag.slug != tag_slug:
            return shortcuts.redirect('tag', tag_pk=tag_pk, tag_slug=tag.slug)
        return self.render_to_response({
            'tag': tag,
        })
