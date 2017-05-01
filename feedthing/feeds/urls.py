from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views
from .api.views import FeedAPIViewSet

router = SimpleRouter()
router.register(r'api', FeedAPIViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^', views.index)
]
