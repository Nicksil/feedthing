import json

from . import views


def ws_connect(message):
    # Accept connection
    message.reply_channel.send({'accept': True})
    # Work out room name from path (ignore slashes)
    # room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    # message.channel_session['room'] = room
    # Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    # Group("chat-%s" % message.channel_session['room']).send({
    #     "text": message['text'],
    # })
    result = views.add_feed(json.loads(message.content['text'])['feedURL'])
    message.reply_channel.send({
        'text': json.dumps(result),
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    # Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
    pass
