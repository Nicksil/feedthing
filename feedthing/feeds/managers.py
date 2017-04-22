import feedparser


def fetch_entries(url):
    parsed = feedparser.parse(url)
    return parsed.get('entries', [])


def prepare_entry(entry, feed):
    return {
        'feed': feed,
        'link': entry.get('link', ''),
        'published': entry.get('published_parsed', None),
        'title': entry.get('title', ''),
    }
