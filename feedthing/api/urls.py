from django.conf.urls import include
from django.conf.urls import url

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'feeds', views.FeedViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
