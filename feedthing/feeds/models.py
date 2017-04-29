"""
feeds.models
~~~~~~~~~~~~
"""

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    """A model for a single Feed
    
    ``last_modified`` - (value from Last-Modified header within HTTP response) is set as a
    character field intentionally. For the time-being, I want to ensure the format mirrors
    that of feedparser to reduce chances of mistakenly handling the request. This may be
    change to a datetime field in the future once I figure out just what the hell it is
    I'm doing.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds'
    )

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(blank=True, max_length=255)
    last_modified = models.CharField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('title',)
        unique_together = (('user', 'href'),)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return self.href


class Entry(TimeStampedModel):
    """A model for a single Entry. A single Feed may have many Entry relations.
    """

    feed = models.ForeignKey(
        Feed,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='entries'
    )

    link = models.URLField(blank=True, max_length=255)
    published = models.DateTimeField()
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('-published',)
        unique_together = (('feed', 'link'),)
