from telethon import TelegramClient, events, utils
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import *
from data import *
import time

client = TelegramClient('session_file', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()

destination = PeerChannel(fwd_channel[0])  # If you like to transfer to more places, add accordingly


@client.on(events.NewMessage)
def my_event_handler(event):
    to_id = event.message.to_id
    printer(event)

    # Group listener
    if to_id.channel_id in listened_groups_id and event.out is False:
        # FWD message to channel
        fwd = client(ForwardMessagesRequest(
            from_peer=event.message.to_id,  # who sent these messages?
            id=[event.message.id],  # which are the messages?
            to_peer=destination  # who are we forwarding them to?
        ))

        # Send Details
        sendMessage(event, destination, type='group', mid=fwd.id)

    # Person listener
    if event.input_sender in listened_persons_id:
        # FWD message to channel
        fwd = client(ForwardMessagesRequest(
            from_peer=event.message.to_id,  # who sent these messages?
            id=[event.message.id],  # which are the messages?
            to_peer=destination  # who are we forwarding them to?
        ))

        # Send Details
        sendMessage(event, destination, type='group', mid=fwd.id)


client.idle()


# Helper classes

def printer(event):
    print('--income new message--')
    print('time: ' + time.time())
    print('sender: ' + str(event.input_sender))
    print('to: ' + str(event.message.to_id))
    print('--EOF--')
    if event.raw_text == '':
        print('message does not contain text')
    else:
        print(event.raw_text)


def composeMessage(event):
    user = event.message.input_sender
    u = client.get_entity(user)
    uid = u.id
    userTitle = u.title

    group = event.message.to_id
    g = client.get_entity(group)
    gid = g.id
    groupTitle = g.title

    return [
        [uid, userTitle],
        [gid, groupTitle]
    ]


def sendMessage(event, d, type, mid):
    compose = composeMessage(event)

    user = """
    Sender name: {0}
    Sender ID: [{1}](tg://user?id={1})
    """.format(compose[0][0], compose[0][1])

    group = """
    Group name: {0}
    Group ID: {1}
    """.format(compose[1][0], compose[1][1])

    result = ''

    if type == 'group':
        # Group Listener
        result = user
    elif type == 'user':
        # User Listener
        result = group
    else:
        result = user + '\r\n' + group

    client(SendMessageRequest(d, result, reply_to_msg_id=mid))
