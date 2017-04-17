from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings

from channel2.video.views import IndexView

urlpatterns = [
    # Index view.
    url(r'^$', IndexView.as_view(root='current'), name='index'),

    # Apps.
    url(r'^account/', include('channel2.account.urls', namespace='account')),
    url(r'^video/', include('channel2.video.urls', namespace='video')),
]

if settings.DEBUG:
    # Other URLs.
    urlpatterns += [
        url(r'^static/(?P<path>.*)', serve,
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
