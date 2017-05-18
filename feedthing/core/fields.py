"""
core.fields
~~~~~~~~~~~

AutoCreatedField,
AutoLastModifiedField: Copyright (c) 2009-2015, Carl Meyer and contributors
                       https://github.com/carljm/django-model-utils/blob/master/model_utils/fields.py
"""

from django.db import models
from django.utils import timezone


class AutoCreatedField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', timezone.now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    def pre_save(self, model_instance, add):
        value = timezone.now()
        setattr(model_instance, self.attname, value)
        return value
