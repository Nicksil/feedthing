from rest_framework import serializers

from ..models import Entry
from ..models import Feed


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('feed', 'link', 'published', 'title')


class FeedHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('entries', 'etag', 'href', 'id', 'last_modified', 'title', 'url', 'user')
