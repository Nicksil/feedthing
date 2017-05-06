from django.conf import settings

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Sequence(lambda n: 'test.email{}@example.com'.format(n))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
