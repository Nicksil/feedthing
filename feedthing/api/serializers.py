from rest_framework import serializers

from feeds.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('href', 'title')
