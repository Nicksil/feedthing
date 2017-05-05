from django.conf.urls import url

from .endpoints.catchall import CatchallEndpoint

urlpatterns = [
    url(
        r'^',
        CatchallEndpoint.as_view(),
        name='photobutton-api-catchall'
    ),
]
