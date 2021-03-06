from django.conf import settings

import factory
import pytz


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'feeds.Feed'

    etag = factory.Faker('word')
    href = factory.Faker('url')
    html_href = factory.Faker('url')
    last_modified = factory.Faker('date_time', tzinfo=pytz.timezone(settings.TIME_ZONE))
    title = factory.Faker('word')


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'feeds.Entry'

    feed = factory.SubFactory(FeedFactory)
    href = factory.Faker('url')
    published = factory.Faker('date_time', tzinfo=pytz.timezone(settings.TIME_ZONE))
    title = factory.Faker('word')
