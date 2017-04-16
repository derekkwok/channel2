from django.conf.urls import url

from channel2.video.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index')
]
