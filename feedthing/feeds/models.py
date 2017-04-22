from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds'
    )

    href = models.URLField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('title',)
        unique_together = (('user', 'href'),)


class Entry(TimeStampedModel):
    feed = models.ForeignKey(
        Feed,
        models.CASCADE,
        related_name='entries'
    )

    link = models.URLField(blank=True, max_length=255)
    published = models.DateTimeField()
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('-published',)
        unique_together = (('feed', 'link'),)
