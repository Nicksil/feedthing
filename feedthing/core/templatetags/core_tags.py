from django.template import Library
from django.utils import dateparse

from core.utils import time_since

register = Library()


@register.filter('core_timesince', is_safe=False)
def core_timesince_filter(value):
    if not value:
        return ''

    if isinstance(value, str):
        try:
            value = dateparse.parse_datetime(value)
        except (TypeError, ValueError):
            value = None

    if value is not None:
        return time_since(value)
    return ''
