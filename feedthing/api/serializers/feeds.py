from rest_framework import serializers

from feeds.models import Entry
from feeds.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('etag', 'href', 'last_modified', 'title', 'url')
        model = Feed


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('href', 'published', 'title', 'url')
        model = Entry
