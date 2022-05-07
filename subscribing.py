import pyrogram
import warnings

from datetime import datetime, timezone

from telegram_config import api_id, api_hash
from google_sheets import get_all_channels, add_post, add_posts, add_channel, get_all_titles, get_idle_titles_account
from search import search_for_channel

warnings.filterwarnings("ignore")

POSTS_CNT = 10  # количество постов, которые стягивает бот сразу после подписки подписке
TIME = 1  # 0.5 - слишком быстро


def main():
    # Инициализация клиента
    client = pyrogram.Client("pyrogram", api_id, api_hash)
    client.start()

    cached_channels = get_all_channels()  # Каналы, на которые клиент уже подписан
    cached_titles = get_all_titles()
    cached_titles = [[cached_titles[i], i] for i in range(len(cached_titles))]
    start = 0

    print("Поехали")
    while True:
        try:
            all_titles = get_all_titles()

            new = [[all_titles[i], i] for i in range(len(all_titles)) if [all_titles[i], i] not in cached_titles]
            if new:
                new = new[0]
                print(new)
                new_title = new[0]

                if new_title[0] != '@':
                    search_result = search_for_channel(new_title)
                    if search_result:
                        print(f"Найден канал: {search_result} по запросу {new_title}")
                        get_idle_titles_account().update_cell(new[1] + 1, 3, search_result)
                        cached_titles = [i for i in cached_titles if i[1] != new[1]]
                        cached_titles.append([search_result, new[1]])
                    else:
                        cached_titles = [i for i in cached_titles if i[1] != new[1]]
                        cached_titles.append(new)
        except Exception as e:
            print(e)


        try:
            to_subscribe = get_all_channels() - cached_channels - {"title"}
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

            try:
                if not any(
                        [channel in cached_channels, channel[1:] in cached_channels, raw_channel in cached_channels]):
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

        try:
            cached_channels.add(raw_channel)
        except Exception as e:
            pass


if __name__ == "__main__":
    main()
