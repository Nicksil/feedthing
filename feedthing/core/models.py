"""In reference to TimeStampedModel: Copyright (c) 2009-2015, Carl Meyer and contributors
(https://github.com/carljm/django-model-utils/blob/master/model_utils/fields.py)
"""
from django.db import models

from . import fields


class TimeStampedModel(models.Model):
    created = fields.AutoCreatedField('created')
    modified = fields.AutoLastModifiedField('modified')

    class Meta:
        abstract = True

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
