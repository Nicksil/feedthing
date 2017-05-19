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
            return self
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
        default = kwargs.get('default', NOT_PROVIDED)
        if default is not NOT_PROVIDED and default is not None:
            if not self.is_type(default):
                self.raise_type_exception(default)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.is_type(value):
            self.raise_type_exception(value)
        super().__set__(instance, value)

    def is_type(self, value):
        return isinstance(value, self.typ)

    def raise_type_exception(self, value):
        raise TypeError('Expected {}, got {}'.format(self.typ, type(value)))


class DateTime(Typed):
    typ = datetime.datetime


class String(Typed):
    typ = str


class URL(String):
    validator = URLValidator()

    def __set__(self, instance, value):
        self.validator(value)
        super().__set__(instance, value)


class User(Typed):
    typ = get_user_model()
