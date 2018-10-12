from typing import List

from django import urls

from channel2.apps.web.views import index_view, tag_create_view

urlpatterns: List = [
    urls.re_path(r'^$', index_view.IndexView.as_view(), name='index'),
    urls.re_path(r'^tag/create/$', tag_create_view.TagCreateView.as_view(), name='tag.create'),
]
