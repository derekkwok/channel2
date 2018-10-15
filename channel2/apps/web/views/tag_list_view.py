from typing import Text

from django.http import request as req_module
from django.http import response as resp_module

from channel2.apps.data.models import tag_model
from channel2.lib import views


class TagListView(views.TemplateView):

    template_name = 'web/pages/tag_list.html'
    tag_type: Text = ''

    def get(self, request: req_module.HttpRequest) -> resp_module.HttpResponse:
        del request  # Unused.
        tags = tag_model.Tag.objects.filter(type=self.tag_type).order_by('name')
        return self.render_to_response({
            'tags': tags,
            'tag_type_description': tag_model.TagType.d[self.tag_type],
        })
