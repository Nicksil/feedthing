from rest_framework.routers import SimpleRouter

from .api.views import EntryAPIViewSet

router = SimpleRouter()
router.register(r'api', EntryAPIViewSet)

urlpatterns = router.urls
