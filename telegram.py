from telethon import TelegramClient, sync, events
from telegram_config import api_id, api_hash

from google_sheets import add_post

client = TelegramClient('telethon', api_id, api_hash)


# Определить массив
channel_list = []

# Хэндлер срабатывает для всех новых сообщений
@client.on(events.NewMessage())
async def normal_handler(event):
    raw = event.message.to_dict()

    try:
        # если сообщение из канала, который нам нужен
        if raw['peer_id']['channel_id'] in channel_list:
            add_post(raw['message', raw['peer_id']['channel_id']])

    except KeyError:
        pass



client.start()
client.run_until_disconnected()