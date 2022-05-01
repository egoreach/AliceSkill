import pyrogram
import warnings
from datetime import datetime, timezone

from telegram_config import api_id, api_hash
from google_sheets import get_all_channels, add_post, add_posts

warnings.filterwarnings("ignore")

POSTS_CNT = 10  # количество постов, которые стягивает бот сразу после подписки подписке
TIME = 1  # 0.5 - слишком быстро


def main():
    # Инициализация клиента
    client = pyrogram.Client("pyrogram", api_id, api_hash)
    client.start()

    cached_channels = set()  # Каналы, на которые клиент уже подписан

    while True:
        try:
            to_subscribe = get_all_channels() - cached_channels
        except TypeError:
            print("TimeOut")

        if to_subscribe:
            print(f"Ёще остались: {to_subscribe}")

        # raw_channel - так, как записано в таблице, channel - то, что нужно отдать функции
        for raw_channel in to_subscribe:
            channel = raw_channel.strip()

            if ('//' in raw_channel or 't.me' in raw_channel) and "+" not in raw_channel:  # если имеем дело с ссылкой на публичный канал
                channel = '@' + channel[channel.index('.me/') + 4:]  # переводим в формат @channel
            elif '+' in raw_channel and raw_channel[0] == "@":
                channel = f"https://t.me/{raw_channel[1:]}"
                print(channel)

            if not any([channel in cached_channels, channel[1:] in cached_channels, raw_channel in cached_channels]):
                try:
                    # собственно, подписка
                    client.join_chat(channel)
                    cached_channels.add(raw_channel)

                    # добавление нескольких подследних постов
                    to_add = []
                    cnt = 0

                    for message in client.get_history(channel):
                        if message.chat.type != 'channel' or cnt == POSTS_CNT:
                            break
                        message_text = message.text if message.text else message.caption
                        if message_text and len([i for i in message_text if i.isdigit() or i.isalpha()]) >= 1:
                            date = datetime.fromtimestamp(message.date, tz=timezone.utc)
                            to_add.append([message_text, '@' + message.sender_chat.username,
                                           f'https://t.me/{message.sender_chat.username}',
                                           str(abs(message.sender_chat.id))[-10:], message.sender_chat.title, str(date),
                                           date.timestamp()])
                            cnt += 1

                    add_posts(list(reversed(to_add)))

                except pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant:
                    print(f"Уже подписан на канал {channel}")
                    cached_channels.add(raw_channel)

                except pyrogram.errors.exceptions.flood_420.FloodWait as e:
                    print(f"Флуд (канал {channel}), {e}")

                except pyrogram.errors.exceptions.bad_request_400.UsernameInvalid:
                    print(f"Имя невалидно: {channel}, {raw_channel}")
                    cached_channels.add(raw_channel)

                except Exception as e:
                    print(e, raw_channel)
                    cached_channels.add(raw_channel)


if __name__ == "__main__":
    main()
