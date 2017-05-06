"""
entries.models
~~~~~~~~~~~~
"""
from django.db import models

from core.models import TimeStampedModel
from feeds.models import Feed


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

    class Meta:
        ordering = ('-published',)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return 'Entry: {}'.format(self.href)
