from typing import List

from django import urls
from django.conf import settings

from channel2.data.models import tag_model
from channel2.views.index_view import IndexView
from channel2.views.tag_create_anime_view import TagCreateAnimeView
from channel2.views.tag_create_view import TagCreateView
from channel2.views.tag_delete_view import TagDeleteView
from channel2.views.tag_list_view import TagListView
from channel2.views.tag_view import TagView

urlpatterns: List = [
    urls.re_path(r'^$', IndexView.as_view(), name='index'),

    # Tag related views.
    urls.re_path(r'^tag/create/$', TagCreateView.as_view(), name='tag.create'),
    urls.re_path(r'^tag/create/anime/$', TagCreateAnimeView.as_view(), name='tag.create.anime'),
    urls.re_path(r'^tag/(?P<tag_pk>\d+)/(?P<tag_slug>[\w-]+)/$', TagView.as_view(), name='tag'),
    urls.re_path(r'^tag/(?P<tag_pk>\d+)/(?P<tag_slug>[\w-]+)/delete/$', TagDeleteView.as_view(), name='tag.delete'),
]


# Create tag type views.
for tag_type in tag_model.TagType.d:
    urlpatterns.append(urls.re_path(
        r'^tag/list/{}/$'.format(tag_type),
        TagListView.as_view(tag_type=tag_type),
        name='tag.list.{}'.format(tag_type)))

if settings.DEBUG:
    from django.conf.urls.static import static  # pylint: disable=ungrouped-imports
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
