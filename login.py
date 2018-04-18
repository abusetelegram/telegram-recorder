from telethon import TelegramClient
from data import *

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
client = TelegramClient('session_file', api_id, api_hash, update_workers=4, spawn_read_thread=False)
password = input('if you have 2FA password, please enter right now.')

if password != '':
    client.start(password=password)
else:
    client.start()
