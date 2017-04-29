from rest_framework import serializers

from ..models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('feed', 'link', 'published', 'title')
