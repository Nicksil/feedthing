from rest_framework import serializers

from entries.models import Entry


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('href', 'published', 'title', 'url')
        model = Entry
