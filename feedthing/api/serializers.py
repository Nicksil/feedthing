from rest_framework import serializers

from feeds.models import Entry
from feeds.models import Feed


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'link', 'published', 'title')


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feed
        fields = ('href', 'id', 'title', 'url', 'user')
