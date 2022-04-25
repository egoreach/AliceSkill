from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel

from telegram_config import api_id, api_hash
from google_sheets import add_post


client = TelegramClient('telethon', api_id, api_hash)


# Только новые сообщения
@client.on(events.NewMessage())
async def new_messages_handler(event):
    try:
        raw_message = event.message.to_dict()  # сырое сообщение

        if not raw_message["from_id"]:
            channel_id = raw_message['peer_id']['channel_id']

            channel_entity = (await client.get_entity(PeerChannel(channel_id))).to_dict()

            # пресловутый @channel
            channel_username = channel_entity['username']
            channel_link = None
            if isinstance(channel_username, str):
                channel_username = "@" + channel_username
                channel_link = f'https://t.me/{channel_username[1:]}'

            channel_id = str(channel_entity['id'])
            channel_title = channel_entity['title']
            message = raw_message['message']
            date = raw_message['date']

            # if is_in_channel_list(channel_username) or is_in_channel_list(channel_id):  # так ли нужно эта проверка (ведь клиент подписан только на то, что нужно, а сообщения обрабатываются только из каналов)
            if message and len([i for i in message if i.isalpha() or i.isdigit()]) >= 1:
                add_post(message, channel_username, channel_link, channel_id, channel_title, str(date))

    # Сообщания не от каналов не имеют поля channel_id
    except KeyError as k:
        print(k)

    except Exception as e:
        print(e)


client.start()
client.run_until_disconnected()
