from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds'
    )

    href = models.URLField(blank=True, default='')
    title = models.CharField(blank=True, default='', max_length=255)

    class Meta:
        ordering = ('title',)
