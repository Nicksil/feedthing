"""
feeds.models
~~~~~~~~~~~~
"""
from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.utils import FriendlyID


class Feed(TimeStampedModel):
    """
    A model for a single Feed
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds',
    )

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(max_length=255)
    last_modified = models.DateTimeField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255)
    uid = models.CharField(blank=True, max_length=255, unique=True)

    class Meta:
        ordering = ('title',)
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
        return 'Feed: {}'.format(self.href)


class Entry(TimeStampedModel):
    """
    A model for a single Entry
    """

    feed = models.ForeignKey(
        Feed,
        models.CASCADE,
        related_name='entries'
    )

    href = models.URLField(max_length=255)
    published = models.DateTimeField(blank=True, null=True)
    read = models.BooleanField(default=False)
    title = models.CharField(blank=True, max_length=255)
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
        return 'Entry: {}'.format(self.href)
