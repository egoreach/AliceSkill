from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel
from telethon import functions
from telethon.tl.functions.messages import ImportChatInviteRequest

from time import sleep
from threading import Thread
from warnings import filterwarnings


from telegram_config import api_id, api_hash
from google_sheets import add_post, is_in_channel_list, get_all_channels

# Чтобы не засорять консоль
# filterwarnings("ignore", category=RuntimeWarning)



cached_channels = set()
def subscribing():
    global cached_channels

    def subscribe_channel(channel):
        try:
            if '@' not in channel and '//' in channel:
                async_to_sync(ImportChatInviteRequest(channel[channel.index('+') + 1:])())()
                cached_channels.add(channel)
            else:
                async_to_sync(functions.channels.JoinChannelRequest(channel)())()
                cached_channels.add(channel)
        except: pass

    for _ in range(10**11):
        print(_)
        now = set(get_all_channels())
        to_subscribe = now - cached_channels
        for channel in to_subscribe:
            subscribe_channel(channel)

        sleep(10)

subscribing()
daemon = Thread(target=subscribing())
daemon.start()


client = TelegramClient('telethon', api_id, api_hash)



# Только новые сообщения
@client.on(events.NewMessage())
async def new_messages_handler(event):
    await client(ImportChatInviteRequest("jgqJYN57NDdlYmNi"))
    try:
        raw_message = event.message.to_dict()  # сырое сообщение
        channel_id = raw_message['peer_id']['channel_id']

        channel_entity = (await client.get_entity(PeerChannel(channel_id))).to_dict()

        # пресловутый @channel
        channel_username = channel_entity['username']
        channel_id = channel_entity['id']

        # if is_in_channel_list(channel_username) or is_in_channel_list(channel_id):  # так ли нужно эта проверка (ведь
        add_post(raw_message['message'], "@" + channel_username if isinstance(channel_username, str) else None, f'https://t.me/{channel_username}' if channel_username else None, channel_id)

    # Сообщания не от каналов не имеют поля channel_id
    except KeyError:
        pass


client.start()
client.run_until_disconnected()


# Подключение к каналу
# await client(ImportChatInviteRequest('jgqJYN57NDdlYmNi'))
# client(JoinChannelRequest("@kruginapole"))