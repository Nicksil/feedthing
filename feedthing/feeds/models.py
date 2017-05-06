"""
feeds.models
~~~~~~~~~~~~
"""
from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    """
    A model for a single Feed
    """

    etag = models.CharField(blank=True, max_length=255)
    href = models.URLField(max_length=255, unique=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(blank=True, editable=False, unique=True)

    class Meta:
        ordering = ('title',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(blank=True, editable=False, unique=True)

    class Meta:
        ordering = ('-published',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __repr__(self):
        return '{}(href=\'{}\')'.format(self.__class__.__name__, self.href)

    def __str__(self):
        return 'Entry: {}'.format(self.href)
