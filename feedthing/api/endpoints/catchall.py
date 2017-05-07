from rest_framework import status

from ..base import Endpoint


class CatchallEndpoint(Endpoint):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.status_code = status.HTTP_404_NOT_FOUND
        response.data['detail'] = 'Nothing exists here.'
        return response
