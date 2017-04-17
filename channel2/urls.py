from django.conf.urls import url, include

from channel2.base.views import static_view
from channel2.video.views import IndexView

urlpatterns = [
    # Index view.
    url(r'^$', IndexView.as_view(root='current'), name='index'),

    # Apps.
    url(r'^account/', include('channel2.account.urls', namespace='account')),
    url(r'^video/', include('channel2.video.urls', namespace='video')),

    # Other URLs.
    url(r'^static/(?P<path>.*)', static_view),
]
