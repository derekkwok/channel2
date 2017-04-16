from django.conf.urls import url, include

from channel2.video.views import IndexView

urlpatterns = [
    # Index view.
    url(r'^$', IndexView.as_view(), name='index'),

    # Apps.
    url(r'^account/', include('channel2.account.urls', namespace='account')),
]
