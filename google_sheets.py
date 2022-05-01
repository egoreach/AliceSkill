import gspread
from time import sleep

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")


def add_post(post, channel, channel_link, channel_id, title, date, unix) -> None:
    sleep(1)
    posts.append_row([post, channel, channel_link, channel_id, title, date, unix])


def add_posts(some_posts):
    sleep(1)
    posts.append_rows(some_posts)


def get_all_channels() -> set:
    sleep(1)
    return set(channels.col_values(1))
