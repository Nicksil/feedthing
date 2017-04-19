import feedparser


def add_feed(url):
    print('Sending request for feed...')
    parsed = feedparser.parse(url)

    print('... received response')
    return {
        'feed_title': parsed.feed.title,
    }
