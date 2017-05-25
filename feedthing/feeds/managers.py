from django.conf import settings

import feedparser

from .models import Entry
from .models import Feed
from core.descriptors import typed
from core.exceptions import FeedManagerError
from core.utils import HTMLCleaner
from core.utils import struct_time_to_datetime


class FeedManager:
    etag = typed.String('etag', default='')
    href = typed.URL('href', default='')
    html_href = typed.URL('html_href', default='')
    last_modified = typed.DateTime('last_modified', default=None)
    title = typed.String('title', default='<NO_TITLE>')
    user = typed.User('user', default=None)

    def __init__(self, feed=None, href=None, user=None):
        # We must have an href value if we're going to query an API
        # We can ascertain a href value from either a Feed object or
        # href parameter.
        if not feed and not href:
            raise FeedManagerError('Must provide a value for `feed` or `href` parameters.')

        if not feed and not user:
            raise FeedManagerError('Must provide a value for `feed` or `user` parameters.')

        self.data = None
        self.feed = feed
        self.user = user
        self.href = href if href else feed.href

        if self.feed:
            self.etag = self.feed.etag
            self.html_href = self.feed.html_href
            self.last_modified = self.feed.last_modified
            self.title = self.feed.title

    def build_request_kwargs(self):
        kwargs = {'agent': settings.USER_AGENT_STR}
        if self.last_modified:
            kwargs['modified'] = self.last_modified.isoformat()
        if self.etag:
            kwargs['etag'] = self.etag
        return kwargs

    def create(self):
        if self.user is None:
            raise FeedManagerError('Must provide a `User` object to create a new `Feed`.')

        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)
        self.validate()
        self._set_fields(self.data)

        # Create new Feed record
        self.feed = Feed.objects.create(**self.to_dict())
        self.feed.users.add(self.user)

        # Create new Feed's Entry records
        [Entry.objects.create(**entry) for entry in EntryManager.parse(self.data.get('entries', []), self.feed)]

        return self.feed

    def fetch_source(self, **kwargs):
        return feedparser.parse(self.href, **kwargs)

    def to_dict(self):
        return {
            'etag': self.etag,
            'href': self.href,
            'html_href': self.html_href,
            'last_modified': self.last_modified,
            'title': self.title,
        }

    def update(self):
        if not self.feed:
            raise FeedManagerError('Must provide a value for `feed` before being able to `update`.')

        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)
        self._set_fields(self.data)

        for k, v in self.to_dict().items():
            setattr(self.feed, k, v)
        self.feed.save()

        entries = EntryManager.parse(self.data.get('entries', []), self.feed)
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

    def validate(self):
        message = None

        if not self.data:
            message = '`self.data` has no value.'
        if 'feed' not in self.data:
            message = '`feed` not in `self.data`.'
        if 'entries' not in self.data:
            message = '`entries` not in `self.data`.'
        if len(self.data.get('entries', [])) < 1:
            message = 'No entries in feed response.'

        if message is not None:
            message = '{}: {}'.format(self.href, message)
            raise FeedManagerError(message)

    def _get_html_href(self, data):
        html_href = ''
        links = data['feed'].get('links', [])

        for link in links:
            if link.get('rel') == 'alternate' and link.get('type') == 'text/html':
                html_href = link['href']
                break

        # There's not always going to be and html href w/in a feedparser payload.
        # And we don't need the value to complete any work.
        # Don't want to raise an exception right now, just return an empty string
        return html_href

    def _set_fields(self, data):
        self.etag = data.get('etag', self.etag)
        self.href = data.get('href', self.href)
        self.html_href = self._get_html_href(data) or self.html_href
        self.title = data['feed'].get('title', self.title)

        if 'modified_parsed' in data:
            self.last_modified = struct_time_to_datetime(data['modified_parsed'])


class EntryManager:
    @classmethod
    def parse(cls, entries, feed):
        parsed = []
        for entry in entries:
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

            parsed.append({
                'content': content,
                'feed': feed,
                'href': href,
                'published': published,
                'summary': summary,
                'title': entry.get('title', '<NO_TITLE>')
            })

        return parsed
