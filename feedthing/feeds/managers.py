from django.conf import settings

import feedparser

from core.descriptors import DateTime
from core.descriptors import String
from core.descriptors import URL
from core.descriptors import User
from core.exceptions import FeedManagerError
from core.utils import HTMLCleaner
from core.utils import now
from core.utils import struct_time_to_datetime
from feeds.models import Entry
from feeds.models import Feed


class FeedManager:
    etag = String('etag', default='')
    href = URL('href', default='')
    html_href = URL('html_href', default='')
    last_fetch = DateTime('last_fetch', default=None)
    last_modified = DateTime('last_modified', default=None)
    title = String('title', default='')
    user = User('user', default=None)

    def __init__(self, feed=None, href=None, user=None):
        self.data = None
        self.feed = feed

        # We must have an href value if we're going to query an API
        # We can ascertain a href value from either a Feed object or
        # href parameter.
        if not feed and not href:
            raise FeedManagerError('Must provide a value for ``feed`` or ``href`` parameters.')

        if not feed and not user:
            raise FeedManagerError('Must provide a value for ``feed`` or ``user`` parameters.')

        if href:
            self.href = href
        else:
            self.href = feed.href

        if self.feed:
            self.etag = self.feed.etag
            self.html_href = self.feed.html_href
            self.last_fetch = self.feed.last_fetch
            self.last_modified = self.feed.last_modified
            self.title = self.feed.title
            self.user = self.feed.user
        else:
            self.etag = ''
            self.title = '<NO_TITLE>'
            self.user = user

    def build_request_kwargs(self):
        kwargs = {'agent': settings.USER_AGENT_STR}
        if self.last_modified:
            kwargs['modified'] = self.last_modified.isoformat()
        if self.etag:
            kwargs['etag'] = self.etag
        return kwargs

    def create(self):
        if self.user is None:
            raise FeedManagerError('Must provide a ``User`` object to create a new ``Feed``.')

        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)
        self._set_fields(self.data)
        self.feed = Feed.objects.create(**self.to_dict())

        [Entry.objects.create(**entry) for entry in self._parse_entries()]

        return self.feed

    def fetch_source(self, **kwargs):
        return feedparser.parse(self.href, **kwargs)

    def to_dict(self):
        return {
            'etag': self.etag,
            'href': self.href,
            'html_href': self.html_href,
            'last_fetch': self.last_fetch,
            'last_modified': self.last_modified,
            'title': self.title,
            'user': self.user,
        }

    def update(self):
        if not self.feed:
            raise FeedManagerError('Must provide a value for ``feed`` before being able to ``update``.')

        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)
        self._set_fields(self.data)

        for k, v in self.to_dict().items():
            setattr(self.feed, k, v)
        self.feed.save()

        entries = self._parse_entries()
        for entry in entries:
            href = entry.pop('href', '')
            if Entry.objects.filter(href=href).exists():
                feed = entry.pop('feed', None)
                entry_obj = Entry.objects.get(href=href, feed=feed)
                for k, v in entry.items():
                    setattr(entry_obj, k, v)
                entry_obj.save()
            else:
                Entry.objects.create(href=href, **entry)

        return self.feed

    def _get_html_href(self, data):
        links = data['feed'].get('links', [])
        for link in links:
            if link.get('rel') == 'alternate' and link.get('type') == 'text/html':
                return link['href']

        # There's not always going to be and html href w/in a feedparser payload.
        # And we don't need the value to complete any work.
        # Don't want to raise an exception right now, just return an empty string
        return ''

    def _parse_entries(self):
        entries_data = self.data.get('entries', [])
        entries = []
        for entry in entries_data:
            if 'feedburner_origlink' in entry:
                href = entry['feedburner_origlink']
            else:
                href = entry.get('link', '')

            if 'published_parsed' in entry:
                published = entry['published_parsed']
            elif 'updated_parsed' in entry:
                published = entry['updated_parsed']
            else:
                published = None

            if published is not None:
                published = struct_time_to_datetime(published)

            content = HTMLCleaner.clean(''.join([c.get('value', '') for c in entry.get('content', [])]))
            summary = HTMLCleaner.clean(entry.get('summary', ''))

            entries.append({
                'content': content,
                'feed': self.feed,
                'href': href,
                'published': published,
                'summary': summary,
                'title': entry.get('title', '<NO_TITLE>')
            })
        return entries

    def _set_fields(self, data):
        _etag = self.etag
        _href = self.href
        _html_href = self.html_href
        _last_fetch = now()
        _last_modified = self.last_modified
        _title = self.title

        if 'etag' in data:
            _etag = data['etag']

        if 'href' in data:
            _href = data['href']

        if 'feed' in data:
            _html_href = self._get_html_href(data) or _html_href

            if _title == '<NO_TITLE>' or not _title and 'title' in data['feed']:
                _title = data['feed']['title']

        if 'modified_parsed' in data:
            _last_modified = struct_time_to_datetime(data['modified_parsed'])

        self.etag = _etag
        self.href = _href
        self.html_href = _html_href
        self.last_fetch = _last_fetch
        self.last_modified = _last_modified
        self.title = _title
