from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()
router.register(
    r'feeds',
    views.FeedViewSet,
    base_name='feed'
).register(
    r'entries',
    views.EntryViewSet,
    base_name='feeds-entry',
    parents_query_lookups=['feed']
)

urlpatterns = router.urls
