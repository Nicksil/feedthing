"""
feeds.models
~~~~~~~~~~~~
"""
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    """
    A model for a single Feed
    """

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(max_length=255, unique=True)
    last_modified = models.DateTimeField(blank=True)
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('title',)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return 'Feed: {}'.format(self.href)
