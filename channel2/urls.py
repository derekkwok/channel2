from typing import List

from django import urls

from channel2.apps.data.models import tag_model
from channel2.apps.web.views.index_view import IndexView
from channel2.apps.web.views.tag_create_anime_view import TagCreateAnimeView
from channel2.apps.web.views.tag_create_view import TagCreateView
from channel2.apps.web.views.tag_list_view import TagListView

urlpatterns: List = [
    urls.re_path(r'^$', IndexView.as_view(), name='index'),

    # Tag related views.
    urls.re_path(r'^tag/create/$', TagCreateView.as_view(), name='tag.create'),
    urls.re_path(r'^tag/create/anime/$', TagCreateAnimeView.as_view(), name='tag.create.anime'),
]


# Create tag type views.
for tag_type in tag_model.TagType.d:
    urlpatterns.append(urls.re_path(
        r'^tag/list/{}/$'.format(tag_type),
        TagListView.as_view(tag_type=tag_type),
        name='tag.list.{}'.format(tag_type)))
