from channels.routing import route

from feeds.consumers import ws_add
from feeds.consumers import ws_disconnect
from feeds.consumers import ws_message

channel_routing = [
    route('websocket.connect', ws_add),
    route('websocket.recieve', ws_message),
    route('websocket.disconnect', ws_disconnect),
]
