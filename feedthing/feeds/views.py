import feedparser


def add_feed(url):
    parsed = feedparser.parse(url)

    if 'feed' in parsed:
        description = parsed['feed'].get('description', '')
        href = parsed['feed'].get('href', '')
        link = parsed['feed'].get('link', '')
        summary = parsed['feed'].get('summary', '')
        title = parsed['feed'].get('title', '')

    return {'feed_title': parsed.feed.title}
