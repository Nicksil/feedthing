from rest_framework.routers import SimpleRouter

from .api.views import FeedAPIViewSet

router = SimpleRouter()
router.register(r'api', FeedAPIViewSet)

urlpatterns = router.urls
