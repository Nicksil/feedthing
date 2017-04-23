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
    base_name='entry',
    parents_query_lookups=['feed']
)

# router.register(
#     r'entries',
#     views.EntryViewSet,
#     base_name='entry'
# )

urlpatterns = router.urls
