from django.http import Http404

from rest_framework.generics import GenericAPIView

from core.exceptions import ResourceDoesNotExist


class Endpoint(GenericAPIView):
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise ResourceDoesNotExist
