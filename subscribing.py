import pyrogram

from time import sleep

from telegram_config import api_id, api_hash
from google_sheets import get_all_channels

TIME = 1  # 0.5 - слишком быстро


def main():
    # Инициализация клиента
    client = pyrogram.Client("pyrogram", api_id, api_hash)
    client.start()

    cached_channels = set()  # Каналы, на которые клиент уже подписан

    while True:
        to_subscribe = get_all_channels() - cached_channels

        if to_subscribe:
            print(f"Ёще остались: {to_subscribe}")

        # raw_channel - так, как записано в таблице, channel - то, что нужно отдать функции
        for raw_channel in to_subscribe:
            channel = raw_channel

            if (
                    '//' in raw_channel or 't.me' in raw_channel) and "+" not in raw_channel:  # если имеем дело с ссылкой на публичный канал
                channel = '@' + channel[channel.index('.me/') + 4:]  # переводим в формат @channel

            try:
                client.join_chat(channel)
                cached_channels.add(raw_channel)
            except pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant:
                # print(f"Уже подписан на канал {channel}")
                cached_channels.add(raw_channel)
            except pyrogram.errors.exceptions.flood_420.FloodWait as e:
                # print(f"Флуд (канал {channel}), {e}")
                pass

            except pyrogram.errors.exceptions.bad_request_400.UsernameInvalid:
                print(f"Канал {channel} не существует")
                cached_channels.add(raw_channel)


            except Exception as e:
                print(e)

        sleep(TIME)
