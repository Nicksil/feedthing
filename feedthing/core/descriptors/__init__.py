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
