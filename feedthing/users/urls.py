from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views
from .api.views import UserAPIViewSet

router = SimpleRouter()
router.register(r'api', UserAPIViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^sign-in/$', views.sign_in, name='sign_in')
]
