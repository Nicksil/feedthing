from rest_framework.routers import SimpleRouter

from .api.views import UserAPIViewSet

router = SimpleRouter()
router.register(r'api', UserAPIViewSet)

urlpatterns = router.urls
