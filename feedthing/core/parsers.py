import feedparser


class FeedParser:
    def __init__(self, data: feedparser.FeedParserDict):
        self.data = data

    @classmethod
    def parse(cls, data: feedparser.FeedParserDict) -> dict:
        _instance = cls(data)
        return _instance._parse()

    def _parse(self) -> dict:
        return {
            'entries': self.data.get('entries', []),
            'etag': self.data.get('etag', ''),
            'href': self.data.get('href', ''),
            'last_modified': self._get_last_modified(),
            'title': self._get_title(),
        }

    def _get_last_modified(self) -> str:
        headers = self.data.get('headers')

        if headers and 'Last-Modified' in headers:
            return headers['Last-Modified']

        return ''

    def _get_title(self) -> str:
        feed = self.data.get('feed')

        if feed and 'title' in feed:
            return feed['title']

        return ''
