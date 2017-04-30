from django.conf.urls import url

from channel2.account import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<token>.*)/$', views.ActivateView.as_view(),
        name='activate'),
]
