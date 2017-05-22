import datetime

from django.contrib.auth import get_user_model
from django.core.validators import URLValidator


class NOT_PROVIDED:
    pass


class Descriptor:
    def __init__(self, name, default=NOT_PROVIDED):
        self.name = name
        self.default = default

    def __get__(self, instance, cls):
        if instance is None:
            return self  # pragma: no cover
        else:
            try:
                return instance.__dict__[self.name]
            except KeyError as e:
                if self.default is not NOT_PROVIDED:
                    return self.default
                raise e

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


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
