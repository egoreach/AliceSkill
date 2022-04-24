import gspread

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")
info = sheet.worksheet("info")


def add_post(post, channel, channel_link, channel_id, title, date) -> None:
    posts.append_row([post, channel, channel_link, channel_id, title, date])
    info.update('B2', int(info.acell('B2').value) + 1)


def get_all_channels() -> set:
    return set(channels.col_values(1))
