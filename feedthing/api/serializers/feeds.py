from rest_framework import serializers

from ..fields import NestedHyperlinkedIdentityField
from feeds.models import Entry
from feeds.models import Feed


class EntryNestedHyperlinkedIdentityField(NestedHyperlinkedIdentityField):
    url_kwarg_attrs = {'entry_id': 'id', 'feed_id': 'feed.id'}
    view_name = 'feedthing-api-v1-entry-details'


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    feed = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        lookup_url_kwarg='feed_id',
        view_name='feedthing-api-v1-feed-details'
    )
    url = EntryNestedHyperlinkedIdentityField()

    class Meta:
        extra_kwargs = {'id': {'read_only': True}}
        fields = (
            'content', 'content_string', 'feed', 'href', 'id', 'published',
            'summary', 'summary_string', 'title', 'url'
        )
        model = Entry


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryNestedHyperlinkedIdentityField(many=True, required=False)
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        lookup_url_kwarg='feed_id',
        view_name='feedthing-api-v1-feed-details',
    )

    class Meta:
        extra_kwargs = {
            'updated': {'read_only': True},
            'id': {'read_only': True},
        }
        fields = (
            'entries', 'etag', 'href', 'html_href', 'id', 'last_modified', 'title',
            'updated', 'url'
        )
        model = Feed
