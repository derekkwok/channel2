from django.conf.urls import url

from channel2.video import views

urlpatterns = [
    url(r'^list/(?P<path>.*)$', views.IndexView.as_view(), name='index'),
]
