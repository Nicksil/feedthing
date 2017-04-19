from channels.routing import route

from feeds.consumers import ws_connect
from feeds.consumers import ws_disconnect
from feeds.consumers import ws_message

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_message),
    route('websocket.disconnect', ws_disconnect),
]
