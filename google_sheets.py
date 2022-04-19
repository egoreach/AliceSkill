import gspread

TABLE = "Database"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

posts = sheet.worksheet("posts")
channels = sheet.worksheet("channels")


def add_post(post, channel):
    posts.append_row([post, channel])

def add_channel(channel):
    channels.append_row([channel])