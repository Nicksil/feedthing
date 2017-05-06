import feedparser
from rest_framework.response import Response

from core.parsers import FeedParser
from feeds.models import Feed
from ..base import Endpoint
from ..serializers.feeds import FeedSerializer


class FeedIndexEndpoint(Endpoint):
    def get(self, request):
        return Response(
            FeedSerializer(
                request.user.feeds.all(),
                context={'request': request},
                many=True,
            ).data
        )

    def post(self, request):
        href = request.data['href']
        if not Feed.objects.filter(href=href, user=request.user).exists():
            feed_data = feedparser.parse(href)
            parsed = FeedParser.parse(feed_data)
            # FIXME: If this link is diff from href used, re-run fetch to get true feed
            entries = parsed.pop('entries')
            request.data.update(parsed)
        serializer = FeedSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
