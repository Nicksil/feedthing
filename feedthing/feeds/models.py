from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='feeds'
    )

    description = models.CharField(max_length=255)
    href = models.URLField()
    link = models.URLField()
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('title',)
