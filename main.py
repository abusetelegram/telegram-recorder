from telethon import TelegramClient, events, utils
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import *
from data import *
import time

client = TelegramClient('session_file', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()


@client.on(events.NewMessage)
def my_event_handler(event):
    to_id = event.message.to_id
    printer(event)

    # Group listener
    if to_id.channel_id in listened_groups_id and event.out is False:
        # FWD message to channel
        client(ForwardMessagesRequest(
            from_peer=event.message.to_id,  # who sent these messages?
            id=[event.message.id],  # which are the messages?
            to_peer=PeerChannel(fwd_channel)  # who are we forwarding them to?
        ))

    # Person listener
    if event.input_sender in listened_persons_id:
        # FWD message to channel
        client(ForwardMessagesRequest(
            from_peer=event.message.to_id,  # who sent these messages?
            id=[event.message.id],  # which are the messages?
            to_peer=PeerChannel(fwd_channel)  # who are we forwarding them to?
        ))


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