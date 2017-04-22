from rest_framework import serializers

from feeds.models import Feed, Entry


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('href', 'title')


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('href', 'published', 'title')
