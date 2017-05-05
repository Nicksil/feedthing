from django.http import HttpResponse

from ..base import Endpoint


class CatchallEndpoint(Endpoint):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(status=404)
