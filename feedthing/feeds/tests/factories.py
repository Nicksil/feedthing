from django.conf import settings

import factory
import pytz

from users.tests.factories import UserFactory


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'feeds.Feed'

    etag = factory.Faker('word')
    href = factory.Faker('url')
    last_modified = factory.Faker('date_time', tzinfo=pytz.timezone(settings.TIME_ZONE))
    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
