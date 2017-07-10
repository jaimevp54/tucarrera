from django.conf.urls import url
from .views import filter_events

urlpatterns = [
    url(r'^filter/$', filter_events, name='filter_events'),
]
