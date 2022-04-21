import gspread

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")

def add_post(post, channel, channel_link, channel_id) -> None:
    posts.append_row([post, channel, channel_link, channel_id])

def get_all_channels():
    return set(channels.col_values(1))

