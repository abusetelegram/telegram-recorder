from telethon import TelegramClient, events, utils
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import *
from data import *

from telethon.tl.functions.channels import GetChannelsRequest
from telethon.tl.functions.users import GetUsersRequest
from telethon.extensions.markdown import parse

client = TelegramClient('session_file', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()

destination = PeerChannel(fwd_channel[0])  # If you like to transfer to more places, add accordingly


@client.on(events.NewMessage(incoming=True))
def my_event_handler(event):
    # Helper classes

    def printer(event):
        print('--income new message--')
        # print('time: ' + time.time())
        print('sender: ' + str(event.input_sender))
        print('to: ' + str(event.message.to_id))
        print('--raw Message--')
        if event.raw_text == '':
            print('message does not contain text')
        else:
            print(event.raw_text)
        print('--EOF--')

    def sendMessage(compose, mtype):
        user = """Sender name: {1}
Sender ID: [{0}](tg://user?id={0})
        """.format(compose[0][0], compose[0][1])

        group = """Group name: {1}
Group ID: {0}
        """.format(compose[1][0], compose[1][1])

        result = ''

        if mtype == 'group':
            # Group Listener
            result = user
        elif mtype == 'user':
            # User Listener
            result = group
        else:
            result = user + '\r\n' + group

        return result

    def compose():
        user = client(GetUsersRequest([event.input_sender]))[0]
        name = ''
        if user.first_name is not None:
            name = name + user.first_name
        if user.last_name is not None:
            name = name + ' ' + user.last_name

        u = [user.id, name]

        group = client(GetChannelsRequest([event.message.to_id])).chats[0]
        g = [group.id, group.title]

        compose = [
            u,
            g
        ]

        return compose

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
        message = sendMessage(compose(), mtype='all')
        # client(SendMessageRequest(destination, message, entities=msg_entities))
        client.send_message(destination, message, parse_mode='md')

    # Person listener
    if event.input_sender.user_id in listened_persons_id:
        # FWD message to channel
        fwd = client(ForwardMessagesRequest(
            from_peer=event.message.to_id,  # who sent these messages?
            id=[event.message.id],  # which are the messages?
            to_peer=destination  # who are we forwarding them to?
        ))

        # Send Details
        message = sendMessage(compose(), mtype='all')
        #client(SendMessageRequest(destination, message))
        client.send_message(destination, message, parse_mode='md')


print('Started, sit and enjoy!')
client.idle()
