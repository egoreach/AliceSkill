from telethon import TelegramClient, events, sync
from telethon import functions

import asyncio

client = TelegramClient('search', 11983547, '6b3179f42f32e8a31b3644523a8c1f8c')

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
    channel = loop.run_until_complete(async_search(query))

    return '@' + channel if channel else None
