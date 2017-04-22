from rest_framework import serializers

from feeds.models import Entry
from feeds.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feed
        fields = ('href', 'title', 'user')


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('href', 'published', 'title')
