from rest_framework import serializers

from feeds.models import Entry
from feeds.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='uid',
        lookup_url_kwarg='feed_uid',
        view_name='feedthing-api-v1-feed-details',
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('etag', 'href', 'last_modified', 'title', 'url', 'user')
        model = Feed


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='uid',
        lookup_url_kwarg='entry_uid',
        view_name='feedthing-api-v1-feed-entry-details',
    )

    class Meta:
        fields = ('href', 'published', 'title', 'url')
        model = Entry
