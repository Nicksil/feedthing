"""
core.utils
~~~~~~~~~~
"""
import datetime
import re
import time

from django.utils import timezone

from bs4 import BeautifulSoup


def ensure_aware(dt):
    """Will convert datetime.datetime instance from naive into aware,
    or return if instance is already aware.
    """
    if timezone.is_aware(dt):
        return dt
    return timezone.make_aware(dt)


def now(aware=True):
    _now = datetime.datetime.now()
    if aware:
        return ensure_aware(_now)
    return _now


def struct_time_to_datetime(s_time: time.struct_time, aware: bool = True) -> datetime.datetime:
    """Will convert time.struct_time instance to datetime.datetime object. Will return
    aware datetime object unless aware = False (default is True).
    """
    dt = datetime.datetime.fromtimestamp(
        time.mktime(s_time)
    )

    if aware:
        return ensure_aware(dt)
    return dt


def time_since(dt: datetime.datetime):
    dt = ensure_aware(dt)
    _now = ensure_aware(datetime.datetime.now())

    delta = _now - dt

    if delta.days == 0:
        return '{}h'.format(int(delta.total_seconds() / 60 / 60))
    return '{}d'.format(int(delta.total_seconds() / 60 / 60 / 24))


class HTMLCleaner:
    def __init__(self, html_str):
        self.soup = BeautifulSoup(html_str, 'html.parser')

    @classmethod
    def clean(cls, html_str):
        instance = cls(html_str)
        instance.clean_attrs()
        instance.del_tags()
        return str(instance.soup)

    def clean_attrs(self):
        remove_attrs = ['class', 'height', 'id', 'sizes', 'style', 'width']
        for tag in self.soup.find_all(True):
            new_attrs = {k: v for k, v in tag.attrs.items() if k not in remove_attrs}
            tag.attrs = new_attrs

    def del_tags(self):
        # feeds.feedburner.com
        for tag in self.soup.find_all(src=re.compile('feeds.feedburner.com')):
            # Check for parent
            parent = tag.parent
            if parent:
                # Now check if tag is only contents of parent
                parent_contents = parent.contents
                # If this tag is the only member in it's parents contents,
                # remove parent as well.
                if len(parent_contents) == 1:
                    parent.decompose()
                else:
                    # else, just remove the tag
                    tag.decompose()
            else:
                tag.decompose()

    @classmethod
    def make_string(cls, html_str):
        instance = cls(html_str)
        return ''.join(list(map(lambda s: s.strip('\n'), instance.soup.strings)))
