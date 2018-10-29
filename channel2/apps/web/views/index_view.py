import datetime

from django.http import request as req_module
from django.http import response as resp_module

from channel2.apps.data.models import tag_model
from channel2.lib import views


class IndexView(views.TemplateView):

    template_name = 'web/pages/index.html'

    def get(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        del request  # Unused.
        tag_name = tag_model.get_anime_season_name(datetime.datetime.now())
        tag = tag_model.Tag.objects.get_or_create(
            name=tag_name,
            type=tag_model.TagType.ANIME_SEASON)[0]
        return self.render_to_response({
            'tags': tag.children.all().order_by('name'),
        })
