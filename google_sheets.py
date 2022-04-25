import gspread
from time import sleep

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")


def add_post(post, channel, channel_link, channel_id, title, date) -> None:
    sleep(1)
    posts.append_row([post, channel, channel_link, channel_id, title, date])


def get_all_channels() -> set:
    sleep(1)
    return set(channels.col_values(1))
