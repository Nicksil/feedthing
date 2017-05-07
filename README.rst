.. image:: https://travis-ci.org/Nicksil/feedthing.svg?branch=master
   :target: https://travis-ci.org/Nicksil/feedthing

.. image:: https://codecov.io/gh/Nicksil/feedthing/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Nicksil/feedthing

Feed Thing
==========

    ...because I just want to read my feeds, that's all.

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

feedparser documentation: https://pythonhosted.org/feedparser/
