import gspread

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")

def add_post(post, channel, channel_link) -> None:
    posts.append_row([post, channel, channel_link])

def is_in_channel_list(channel: str) -> bool:
    return channel in channels.col_values(1)

