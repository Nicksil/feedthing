from django.shortcuts import render

from .api.serializers import FeedHyperlinkedModelSerializer


def index(request):
    payload = {}
    user = request.user

    if user.is_authenticated:
        feeds = user.feeds.all()
        serializer = FeedHyperlinkedModelSerializer(feeds, context={'request': request}, many=True)
        payload = {'feeds': serializer.data}

    return render(request, 'index.html', payload)
