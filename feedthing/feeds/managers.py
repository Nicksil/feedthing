import feedparser


def fetch_entries(url):
    parsed = feedparser.parse(url)
    return parsed.get('entries', [])
