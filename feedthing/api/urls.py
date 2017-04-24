from django.conf.urls import include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'feeds', views.FeedViewSet, base_name='feed')

urlpatterns = [
    url(r'^feeds/(?P<feed_pk>[^/.]+)/entries/$', views.EntryListAPIView.as_view(), name='entry-list'),
    url(r'^feeds/(?P<feed_pk>[^/.]+)/entries/(?P<pk>[^/.]+)/$', views.EntryDetailAPIView.as_view()),
    url(r'^', include(router.urls)),
]
