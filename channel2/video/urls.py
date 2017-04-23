from django.conf.urls import url

from channel2.video import views

urlpatterns = [
    url(r'^file/(?P<path>.*)/', views.FileView.as_view(), name='file'),
    url(r'^link/(?P<path>.*)/(?P<name>.*)', views.LinkView.as_view(),
        name='link'),
]
