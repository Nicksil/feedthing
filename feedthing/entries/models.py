from django.db import models

from core.models import TimeStampedModel
from feeds.models import Feed


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

    href = models.URLField(max_length=255)
    published = models.DateTimeField()
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('-published',)
        unique_together = (('feed', 'href'),)
