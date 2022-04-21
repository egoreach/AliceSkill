from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel

from time import sleep

from telegram_config import api_id, api_hash
from google_sheets import add_post


client = TelegramClient('telethon', api_id, api_hash)


# Только новые сообщения
@client.on(events.NewMessage())
async def new_messages_handler(event):
    try:
        raw_message = event.message.to_dict()  # сырое сообщение
        channel_id = raw_message['peer_id']['channel_id']

        channel_entity = (await client.get_entity(PeerChannel(channel_id))).to_dict()

        # пресловутый @channel
        channel_username = channel_entity['username']
        channel_id = channel_entity['id']

        # if is_in_channel_list(channel_username) or is_in_channel_list(channel_id):  # так ли нужно эта проверка (ведь клиент подписан только на то, что нужно, а сообщения обрабатываются только из каналов)
        add_post(raw_message['message'], "@" + channel_username if isinstance(channel_username, str) else None, f'https://t.me/{channel_username}' if channel_username else None, channel_id)

    # Сообщания не от каналов не имеют поля channel_id
    except KeyError:
        pass


client.start()
client.run_until_disconnected()
