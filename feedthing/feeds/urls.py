from rest_framework.routers import SimpleRouter

from .api.views import EntryAPIViewSet
from .api.views import FeedAPIViewSet

router = SimpleRouter()
router.register(r'api', JobAPIViewSet)

urlpatterns = router.urls
