Feed Thing
==========

    ...because I just want to read my feeds. That's it.

Version
~~~~~~~

0.00.0.11a (everything will change)

TODO
~~~~

- Implement bandwidth courtesies:
  - ETag inspection (https://pythonhosted.org/feedparser/http-etag.html#etag-and-last-modified-headers)
  - Last-Modified header inspection (https://pythonhosted.org/feedparser/http-etag.html#using-last-modified-headers-to-reduce-bandwidth)
  - What do if no ETag, Last-Modified header?
- Check response status code for unreachable feeds; handle this case
- Add feature to use OPML file for adding feeds
- Add feature allowing multiple feed URLs in a single request


Reference
~~~~~~~~~

feedparser.FeedParserDict Structure

::

    # feedparser.FeedParserDict contents (some text 'snipped' for brevity)
    {
        'bozo': 0,
        'encoding': 'utf-8',
        'entries': [
            {
                'author': 'Charlotte Mays',
                'author_detail': {
                    'name': 'Charlotte Mays'
                },
                'authors': [
                    {
                        'name': 'Charlotte Mays'
                    }
                ],
                'content': [
                    {
                        'base': 'https://www.caktusgroup.com/feeds/tags/django/',
                        'language': 'en',
                        'type': 'text/html',
                        'value': '<html><head></head><body><div class="document">... *snip* ...</div>\n</body></html>'
                    }
                ],
                'guidislink': False,
                'id': 'https://www.caktusgroup.com/blog/2017/01/11/new-year-new-python-3-6/',
                'link': 'https://www.caktusgroup.com/blog/2017/01/11/new-year-new-python-3-6/',
                'links': [
                    {
                        'href': 'https://www.caktusgroup.com/blog/2017/01/11/new-year-new-python-3-6/',
                        'rel': 'alternate',
                        'type': 'text/html'
                    }
                ],
                'published': 'Wed, 11 Jan 2017 19:44:14 +0000',
                'published_parsed': time.struct_time(tm_year=2017, tm_mon=1, tm_mday=11, tm_hour=19, tm_min=44, tm_sec=14, tm_wday=2, tm_yday=11, tm_isdst=0),
                'summary': 'Python 3.6 was released in the tail end of 2016. Read on for a few highlights from this release. New module: secrets Python 3.6 introduces a new module in the standard library called secrets. While the random module has long existed to provide us with pseudo-random numbers suitable for applications like modeling and simulation, these...',
                'summary_detail': {
                    'base': 'https://www.caktusgroup.com/feeds/tags/django/',
                    'language': 'en',
                    'type': 'text/html',
                    'value': 'Python 3.6 was released in the tail end of 2016. Read on for a few highlights from this release. New module: secrets Python 3.6 introduces a new module in the standard library called secrets. While the random module has long existed to provide us with pseudo-random numbers suitable for applications like modeling and simulation, these...'
                },
                'title': 'New year, new Python: Python 3.6',
                'title_detail': {
                    'base': 'https://www.caktusgroup.com/feeds/tags/django/',
                    'language': 'en',
                    'type': 'text/plain',
                    'value': 'New year, new Python: Python 3.6'
                }
            }
        ],
        'feed': {
            'language': 'en-us',
            'link': 'https://www.caktusgroup.com/blog/tags/django/',
            'links': [
                {
                    'href': 'https://www.caktusgroup.com/blog/tags/django/',
                    'rel': 'alternate',
                    'type': 'text/html'
                },
                {
                    'href': 'https://www.caktusgroup.com/feeds/tags/django/',
                    'rel': 'self',
                    'type': 'application/atom+xml'
                }
            ],
            'subtitle': 'Blog | Django Web Development | Raleigh Durham Chapel Hill | Caktus Consulting Group',
            'subtitle_detail': {
                'base': 'https://www.caktusgroup.com/feeds/tags/django/',
                'language': 'en',
                'type': 'text/html',
                'value': 'Blog | Django Web Development | Raleigh Durham Chapel Hill | Caktus Consulting Group'
            },
            'title': 'Caktus Blog',
            'title_detail': {
                'base': 'https://www.caktusgroup.com/feeds/tags/django/',
                'language': 'en',
                'type': 'text/plain',
                'value': 'Caktus Blog'
            },
            'updated': 'Wed, 05 Apr 2017 12:00:00 +0000',
            'updated_parsed': time.struct_time(tm_year=2017, tm_mon=4, tm_mday=5, tm_hour=12, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=95, tm_isdst=0)
        },
        'headers': {
            'Cache-Control': 'max-age=3600',
            'Connection': 'close',
            'Content-Language': 'en',
            'Content-Type': 'application/rss+xml; charset=utf-8',
            'Date': 'Sat, 22 Apr 2017 04:39:46 GMT',
            'Expires': 'Sat, 22 Apr 2017 05:06:54 GMT',
            'Last-Modified': 'Wed, 05 Apr 2017 12:00:00 GMT',
            'P3P': 'CP="Hello IE"',
            'Server': 'nginx/1.10.3',
            'Transfer-Encoding': 'chunked',
            'Vary': 'Accept-Language, Cookie',
            'X-Frame-Options': 'DENY',
            'strict-transport-security': 'max-age=31536000',
            'x-content-type-options': 'nosniff',
            'x-xss-protection': '1; mode=block'
        },
        'href': 'https://www.caktusgroup.com/feeds/tags/django/',
        'namespaces': {
            '': 'http://www.w3.org/2005/Atom',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'dc': 'http://purl.org/dc/elements/1.1/'
        },
        'status': 301,
        'updated': 'Wed, 05 Apr 2017 12:00:00 GMT',
        'updated_parsed': time.struct_time(tm_year=2017, tm_mon=4, tm_mday=5, tm_hour=12, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=95, tm_isdst=0),
        'version': 'rss20'
    }
