from rest_framework import serializers
from rest_framework.reverse import reverse


class NestedHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    queryset = None
    url_kwarg_attrs = {}
    view_name = None

    def __init__(self, **kwargs):
        self.url_kwarg_attrs = kwargs.pop('url_kwarg_attrs', self.url_kwarg_attrs)
        super().__init__(view_name=self.view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {}

        for url_kwarg, attr_str in self.url_kwarg_attrs.items():
            _obj = obj

            for _attr in attr_str.split('.'):
                _obj = getattr(_obj, _attr)

            url_kwargs[url_kwarg] = _obj

        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
