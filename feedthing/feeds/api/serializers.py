from rest_framework import serializers

from ..models import Feed
from entries.api.serializers import EntryHyperlinkedModelSerializer


class FeedHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryHyperlinkedModelSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ('entries', 'etag', 'href', 'last_modified', 'title', 'url')
