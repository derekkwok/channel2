from django import shortcuts
from django.http import request as req_module
from django.http import response as resp_module

from channel2.forms import tag_create_anime_form
from channel2.lib import views


class TagCreateAnimeView(views.TemplateView):

    template_name = 'web/pages/tag_create_anime.html'

    def get(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        del request  # Unused.
        form = tag_create_anime_form.TagCreateAnimeForm()
        return self.render_to_response({
            'form': form,
        })

    def post(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        form = tag_create_anime_form.TagCreateAnimeForm(data=request.POST)
        if form.is_valid():
            tag = form.save()
            return shortcuts.redirect('tag', tag_pk=tag.pk, tag_slug=tag.slug)
        return self.render_to_response({
            'form': form,
        })
