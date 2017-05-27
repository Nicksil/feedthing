"""
feeds.models
~~~~~~~~~~~~
"""
import uuid

from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    """A model for a single Feed"""

    # Primary key
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(unique=True)
    html_href = models.URLField(blank=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255)
    updated = models.DateTimeField(blank=True, null=True)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.href)


class Entry(TimeStampedModel):
    """A model for a single Entry"""

    # Primary key
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    # Relationships
    feed = models.ForeignKey(
        Feed,
        models.CASCADE,
        related_name='entries'
    )

    content = models.TextField(blank=True)
    content_string = models.TextField(blank=True)
    href = models.URLField()
    published = models.DateTimeField(blank=True, null=True)
    summary = models.TextField(blank=True)
    summary_string = models.TextField(blank=True)
    title = models.TextField(blank=True)

    class Meta:
        ordering = ('-published',)
        unique_together = (('feed', 'href'),)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.href)
