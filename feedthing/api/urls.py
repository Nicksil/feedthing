# from django.conf.urls import include
# from django.conf.urls import url

# from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

# router = routers.DefaultRouter()
# router.register(r'feeds', views.FeedViewSet)

router = ExtendedDefaultRouter()
router.register(r'feeds', views.FeedViewSet)
router.register(r'entries', views.EntryViewSet)

# urlpatterns = [
#     url(r'^', include(router.urls), name='api'),
# ]

urlpatterns = router.urls
