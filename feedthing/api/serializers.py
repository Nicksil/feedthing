from rest_framework import serializers

from feeds.models import Entry
from feeds.models import Feed


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'link', 'published', 'title')


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='feed_pk',
        view_name='entry-list',
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feed
        fields = ('entries', 'etag', 'href', 'id', 'last_modified', 'title', 'url', 'user')
