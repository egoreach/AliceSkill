import time
import gspread

TABLE = "Database"
SHEET = "posts"

spider = gspread.service_account("service_account.json")
sheet = spider.open(TABLE)

worksheet = sheet.worksheet(SHEET)


def add_post(post, channel):
    time.sleep(1)
    worksheet.append_row([post, channel])


