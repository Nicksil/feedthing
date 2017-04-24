from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'feeds', views.FeedViewSet, base_name='feed')
router.register(r'entries', views.EntryViewSet, base_name='entry')
urlpatterns = router.urls
