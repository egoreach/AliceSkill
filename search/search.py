from telethon import events
from telethon.sync import TelegramClient
from telethon import functions

import asyncio

client = TelegramClient('search', 7891326, 'b626fc3516cdef753a9d27dcf096fd25')

is_started = False
async def async_search(q):
    global is_started

    if not is_started:
        await client.start()
        is_started = True

    try:
        result = (await client(functions.contacts.SearchRequest(q, limit=100))).to_dict()['chats']
        for i in result:
            if not i['megagroup'] and not i['gigagroup']:
                return i['username']
    except Exception as e:
        print(e, q)

loop = asyncio.get_event_loop()

def search_for_channel(query):
    try:
        channel = loop.run_until_complete(async_search(query))

        return '@' + channel if channel else None

    except Exception as e:
        print(e)
