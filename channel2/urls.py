from typing import List

from django import urls

from channel2.apps.web.views import index_view

urlpatterns: List = [
    urls.re_path(r'^$', index_view.IndexView.as_view(), name='index')
]
