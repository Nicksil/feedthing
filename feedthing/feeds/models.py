"""
feeds.models
~~~~~~~~~~~~
"""
import uuid

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.utils import FriendlyID
from core.utils import now


class Feed(TimeStampedModel):
    """
    A model for a single Feed
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds'
    )

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField()
    html_href = models.URLField(blank=True)
    last_fetch = models.DateTimeField(default=now)
    last_modified = models.DateTimeField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255)
    uid = models.CharField(blank=True, max_length=255, unique=True)

    class Meta:
        unique_together = (('href', 'user'),)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.uid:
            self.uid = FriendlyID.encode(self.id)
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.href)


class Entry(TimeStampedModel):
    """
    A model for a single Entry
    """

    feed = models.ForeignKey(
        Feed,
        models.CASCADE,
        related_name='entries'
    )

    href = models.URLField()
    published = models.DateTimeField(blank=True, null=True)
    read = models.BooleanField(default=False)
    title = models.TextField(blank=True)
    uid = models.CharField(blank=True, max_length=255, unique=True)

    class Meta:
        ordering = ('-published',)
        unique_together = (('feed', 'href'),)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.uid:
            self.uid = FriendlyID.encode(self.id)
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.href)


class Content(TimeStampedModel):
    """
    A model for a single Content element.
    An Entry may have many Content objects.
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )

    entry = models.ForeignKey(
        Entry,
        models.CASCADE,
        related_name='contents'
    )

    base = models.URLField(blank=True)
    content_type = models.CharField(blank=True, max_length=255)
    language = models.CharField(blank=True, max_length=255)
    value = models.TextField(blank=True)
