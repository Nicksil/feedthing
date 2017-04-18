from channels.routing import route

channel_routing = [
    route('http.request', 'feeds.consumers.http_consumer'),
]
