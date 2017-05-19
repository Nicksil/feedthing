from rest_framework import serializers

from ..fields import NestedHyperlinkedIdentityField
from core.utils import time_since
from feeds.models import Content
from feeds.models import Entry
from feeds.models import Feed


class ContentNestedHyperlinkedIdentityField(NestedHyperlinkedIdentityField):
    url_kwarg_attrs = {'entry_uid': 'entry.uid', 'feed_uid': 'feed.uid', 'content_uid': 'id'}
    view_name = 'feedthing-api-v1-content-details'


class ContentSerializer(serializers.ModelSerializer):
    url = ContentNestedHyperlinkedIdentityField()

    class Meta:
        extra_kwargs = {'uid': {'read_only': True}}
        fields = ('base', 'content_type', 'entry', 'id', 'language', 'url', 'value')
        model = Content


class EntryNestedHyperlinkedIdentityField(NestedHyperlinkedIdentityField):
    url_kwarg_attrs = {'entry_uid': 'uid', 'feed_uid': 'feed.uid'}
    view_name = 'feedthing-api-v1-entry-details'


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    natural_published = serializers.SerializerMethodField()
    url = EntryNestedHyperlinkedIdentityField()

    class Meta:
        extra_kwargs = {
            'contents': {'required': False},
            'uid': {'read_only': True}
        }
        fields = ('contents', 'href', 'natural_published', 'published', 'read', 'title', 'uid', 'url')
        model = Entry

    def get_natural_published(self, obj):
        return time_since(obj.published)


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryNestedHyperlinkedIdentityField(many=True, required=False)
    natural_last_fetch = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        lookup_field='uid',
        lookup_url_kwarg='feed_uid',
        view_name='feedthing-api-v1-feed-details',
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        extra_kwargs = {
            'last_fetch': {'read_only': True},
            'uid': {'read_only': True}
        }
        fields = (
            'entries', 'etag', 'href', 'html_href', 'last_fetch', 'last_modified',
            'natural_last_fetch', 'title', 'uid', 'url', 'user'
        )
        model = Feed

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['entries'] = EntrySerializer(
            instance.entries.all(),
            context={'request': self.context['request']},
            many=True).data
        return representation

    def get_natural_last_fetch(self, feed):
        return time_since(feed.last_fetch)
