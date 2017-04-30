from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.static import serve

from channel2.video.views import DirectoryView

urlpatterns = [
    # Index URL.
    url(r'^$', RedirectView.as_view(pattern_name='index')),
    url(r'^Current/$', DirectoryView.as_view(), {'path': 'Current'},
        name='index'),

    # Apps.
    url(r'^account/', include('channel2.account.urls', namespace='account')),
    url(r'^admin/', admin.site.urls),
    url(r'^video/', include('channel2.video.urls', namespace='video')),

    # Directory view.
    url(r'^(?P<path>.*)/$', DirectoryView.as_view(), name='directory'),
]

if settings.DEBUG:
    # Other URLs.
    urlpatterns += [
        url(r'^media/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
