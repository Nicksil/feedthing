from rest_framework import viewsets

from ..models import Entry
from .serializers import EntryHyperlinkedModelSerializer


class EntryAPIViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryHyperlinkedModelSerializer
