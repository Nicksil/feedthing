from typing import Optional
from typing import Type
import datetime
import time

from django.contrib.auth.base_user import AbstractBaseUser

import feedparser


from .utils import ensure_aware


class FeedDataManager:
    def __init__(self, href: str, user: Type[AbstractBaseUser] = None) -> None:
        self.data = feedparser.FeedParserDict()
        self.href = href
        self.user = user

    @classmethod
    def fetch(cls, href: str, user: Type[AbstractBaseUser] = None) -> dict:
        mgr = cls(href, user=user)
        mgr.fetch_data()

        return mgr.to_internal()

    def fetch_data(self) -> feedparser.FeedParserDict:
        self.data = feedparser.parse(self.href)
        return self.data

    def to_internal(self) -> dict:
        return {
            'etag': self.data.get('etag', ''),
            'href': self.href,
            'last_modified': self._get_last_modified(),
            'title': self.data['feed'].get('title', ''),
            'user': self.user,
        }

    def _get_last_modified(self) -> Optional[datetime.datetime]:
        last_modified = self.data.get('modified_parsed', None)

        if last_modified is not None:
            return ensure_aware(
                datetime.datetime.fromtimestamp(
                    time.mktime(last_modified)
                )
            )

        return None
