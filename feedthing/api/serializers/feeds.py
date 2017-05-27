from rest_framework import serializers

from ..fields import NestedHyperlinkedIdentityField
from core.utils import time_since
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
    natural_published = serializers.SerializerMethodField()
    url = EntryNestedHyperlinkedIdentityField()

    class Meta:
        extra_kwargs = {'id': {'read_only': True}}
        fields = (
            'content', 'content_string', 'feed', 'href', 'id', 'natural_published',
            'published', 'summary', 'summary_string', 'title', 'url'
        )
        model = Entry

    def get_natural_published(self, obj):
        result = ''
        if obj.published:
            result = time_since(obj.published)
        return result


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['entries'] = EntrySerializer(
            instance.entries.all(),
            context={'request': self.context['request']},
            many=True).data
        return representation
