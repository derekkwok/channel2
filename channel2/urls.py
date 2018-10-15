from typing import List

from django import urls

from channel2.apps.data.models import tag_model
from channel2.apps.web.views import index_view, tag_create_view, tag_list_view

urlpatterns: List = [
    urls.re_path(r'^$', index_view.IndexView.as_view(), name='index'),
    urls.re_path(r'^tag/create/$', tag_create_view.TagCreateView.as_view(), name='tag.create'),
]


# Create tag type views.
for tag_type in tag_model.TagType.d:
    urlpatterns.append(urls.re_path(
        r'^tag/list/{}/$'.format(tag_type),
        tag_list_view.TagListView.as_view(tag_type=tag_type),
        name='tag.list.{}'.format(tag_type)))
