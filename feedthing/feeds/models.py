"""
feeds.models
~~~~~~~~~~~~
"""
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    """
    A model for a single Feed
    
    ``last_modified`` - (value from Last-Modified header within HTTP response) is set as a
    character field intentionally. For the time-being, I want to ensure the format mirrors
    that of feedparser to reduce chances of mistakenly handling the request. This may be
    change to a datetime field in the future once I figure out just what the hell it is
    I'm doing.
    """

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(max_length=255, unique=True)
    last_modified = models.CharField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('title',)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return self.href
