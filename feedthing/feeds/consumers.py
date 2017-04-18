from channels import Group


def ws_add(message):
    message.reply_channel.send({'accept': True})
    Group('chat').add(message.reply_channel)


def ws_message(message):
    Group('chat').send({
        'text': '[user] {}'.format(message.content['text']),
    })


def ws_disconnect(message):
    Group('chat').discard(message.reply_channel)
