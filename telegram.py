from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel
from telethon import functions
from telethon.tl.functions.messages import ImportChatInviteRequest

from telegram_config import api_id, api_hash
from google_sheets import add_post, is_in_channel_list, get_channels


client = TelegramClient('telethon', api_id, api_hash)


# Только новые сообщения
@client.on(events.NewMessage())
async def new_messages_handler(event):
    try:
        raw_message = event.message.to_dict()  # сырое сообщение
        channel_id = raw_message['peer_id']['channel_id']

        # пресловутый @channel
        channel_username = '@' + (await client.get_entity(PeerChannel(channel_id))).to_dict()['username']

        if is_in_channel_list(channel_username):
            add_post(raw_message['message'], channel_username, f'https://t.me/{channel_usernameх[1:]}')

    # Сообщания не от каналов не имеют поля channel_id
    except KeyError:
        pass


client.start()
client.run_until_disconnected()


# Подключение к каналу
# await client(ImportChatInviteRequest('jgqJYN57NDdlYmNi'))
# client(JoinChannelRequest(channel))