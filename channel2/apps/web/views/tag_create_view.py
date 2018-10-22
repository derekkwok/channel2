from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module

from channel2.apps.web.forms import tag_form
from channel2.lib import views


class TagCreateView(views.TemplateView):

    template_name = 'web/pages/tag_create.html'

    def get(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        del request  # Unused.
        return self.render_to_response({
            'form': tag_form.TagForm()
        })

    def post(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        form = tag_form.TagForm(data=request.POST)
        if form.is_valid():
            tag = form.save()
            return shortcuts.redirect('tag', tag_pk=tag.pk, tag_slug=tag.slug)
        return self.render_to_response({
            'form': form,
        })
