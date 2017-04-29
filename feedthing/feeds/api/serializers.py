from rest_framework import serializers

from ..models import Feed


class FeedHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('entries', 'etag', 'href', 'id', 'last_modified', 'title', 'url', 'user')
