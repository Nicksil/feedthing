from rest_framework import serializers
from rest_framework.reverse import reverse


class NestedHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    view_name = None
    queryset = None

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'entry_uid': obj.uid,
            'feed_uid': obj.feed.uid,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
