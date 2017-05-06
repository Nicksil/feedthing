from rest_framework import serializers

from feeds.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('etag', 'href', 'last_modified', 'title', 'url')
        model = Feed
