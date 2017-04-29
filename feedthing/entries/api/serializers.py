from rest_framework import serializers

from ..models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('feed', 'href', 'published', 'title', 'url')
