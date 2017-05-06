"""
feeds.models
~~~~~~~~~~~~
"""
import uuid

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
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ('title',)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return 'Feed: {}'.format(self.href)


class Entry(TimeStampedModel):
    """
    A model for a single Entry. A single Feed may have many Entry relations.
    """

    feed = models.ForeignKey(
        Feed,
        models.CASCADE,
        related_name='entries'
    )

    href = models.URLField(max_length=255, unique=True)
    published = models.DateTimeField()
    title = models.CharField(blank=True, max_length=255)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ('-published',)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return 'Entry: {}'.format(self.href)
