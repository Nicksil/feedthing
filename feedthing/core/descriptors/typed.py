import datetime

from django.contrib.auth import get_user_model
from django.core.validators import URLValidator

from . import Descriptor
from . import NOT_PROVIDED


class Typed(Descriptor):
    typ = object

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.default is not NOT_PROVIDED:
            self.validate(self.default)

    def __set__(self, instance, value):
        self.validate(value)
        super().__set__(instance, value)

    def is_type(self, value):
        return isinstance(value, self.typ)

    def raise_type_exception(self, value):
        raise TypeError('Expected {}, got {}.'.format(self.typ, type(value)))

    def validate(self, value):
        if value is None:
            return value
        if not self.is_type(value):
            self.raise_type_exception(value)


class DateTime(Typed):
    typ = datetime.datetime


class String(Typed):
    typ = str


class URL(String):
    validator = URLValidator()

    def validate(self, value):
        super().validate(value)
        if len(value):
            self.validator(value)


class User(Typed):
    typ = get_user_model()
