from typing import Text

from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module
from django.shortcuts import get_object_or_404

from channel2.data.models import tag_model
from channel2.forms import tag_form
from channel2.lib import views


class TagEditView(views.TemplateView):

    template_name = 'web/pages/tag_edit.html'

    def get(self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del request  # Unused.
        del tag_slug  # Unused.
        tag = get_object_or_404(tag_model.Tag, pk=tag_pk)
        return self.render_to_response({
            'form': tag_form.TagForm(instance=tag),
            'tag': tag,
        })

    def post(
            self,
            request: req_module.HttpRequest,
            tag_pk: int,
            tag_slug: Text) -> resp_module.HttpResponse:
        del tag_slug  # Unused.
        tag = get_object_or_404(tag_model.Tag, pk=tag_pk)
        form = tag_form.TagForm(instance=tag, data=request.POST)
        if form.is_valid():
            tag = form.save()
            return shortcuts.redirect('tag', tag_pk=tag.pk, tag_slug=tag.slug)
        return self.render_to_response({
            'form': form,
            'tag': tag,
        })
