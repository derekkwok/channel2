from django.conf.urls import url

from channel2.video import views

urlpatterns = [
    url(r'^anime/(?P<path>.*)?$', views.IndexView.as_view(root='anime'),
        name='anime'),
    url(r'^current/(?P<path>.*)?$', views.IndexView.as_view(root='current'),
        name='current'),
    url(r'^movies/(?P<path>.*)?$', views.IndexView.as_view(root='movies'),
        name='movies'),
]
