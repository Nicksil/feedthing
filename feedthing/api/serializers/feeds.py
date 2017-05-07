from rest_framework import serializers

from ..fields import NestedHyperlinkedIdentityField
from feeds.models import Entry
from feeds.models import Feed


class EntryNestedHyperlinkedIdentityField(NestedHyperlinkedIdentityField):
    url_kwarg_attrs = {'entry_uid': 'uid', 'feed_uid': 'feed.uid'}
    view_name = 'feedthing-api-v1-entry-details'


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    url = EntryNestedHyperlinkedIdentityField()

    class Meta:
        fields = ('href', 'published', 'title', 'url')
        model = Entry


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryNestedHyperlinkedIdentityField(many=True)
    url = serializers.HyperlinkedIdentityField(
        lookup_field='uid',
        lookup_url_kwarg='feed_uid',
        view_name='feedthing-api-v1-feed-details',
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('entries', 'etag', 'href', 'last_modified', 'title', 'url', 'user')
        model = Feed
