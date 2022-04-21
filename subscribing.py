import pyrogram

from time import sleep

from telegram_config import api_id, api_hash
from google_sheets import get_all_channel

client = pyrogram.Client("pyrogram", api_id, api_hash)
client.start()


cached_channels = set()
def main():
    for _ in range(10**12):
        to_subscribe = get_all_channel() - cached_channels
        for channel in to_subscribe:
            if '//' in channel and "+" not in channel:
                channel = '@' + channel[channel.index('.me/') + 4:]

            try:
                client.join_chat(channel)
                cached_channels.add(channel)
            except pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant:
                print(f"Уже подписан на канал {channel}")
            except pyrogram.errors.exceptions.flood_420.FloodWait:
                print(f"Флуд (канал {channel})")
                print(channel)
            except Exception as e:
                print(e)
                print(channel)
        sleep(5)

main()
