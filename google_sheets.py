import gspread
from time import sleep


TABLE = "Database"


first_account = gspread.service_account("first.json")
first_table = first_account.open(TABLE)

first_posts = first_table.worksheet("posts")
first_channels = first_table.worksheet("channels")


second_account = gspread.service_account("second.json")
second_table = second_account.open(TABLE)

second_posts = second_table.worksheet("posts")
second_channels = second_table.worksheet("channels")


third_account = gspread.service_account("third.json")
third_table = third_account.open(TABLE)

third_posts = third_table.worksheet("posts")
third_channels = third_table.worksheet("channels")


fourth_account = gspread.service_account("fourth.json")
fourth_table = fourth_account.open(TABLE)

fourth_posts = fourth_table.worksheet("posts")
fourth_channels = fourth_table.worksheet("channels")

with open("current.txt", "w") as f:
    f.write(str(len(first_posts.col_values(1))))


def add_post(post, channel, channel_link, channel_id, title, date, unix) -> None:
    sleep(1)

    first_posts.append_row([post, channel, channel_link, channel_id, title, date, unix])

    with open("current.txt", "r+") as f:
        current_post_number = int(f.read())
        current_post_number += 1
    with open("current.txt", "w") as f:
        f.write(str(current_post_number))


    cell = second_channels.find(channel)
    value = third_channels.cell(cell.row, cell.col + 1).value

    fourth_channels.update_cell(cell.row, cell.col + 1, value + "," + str(current_post_number) if value else str(current_post_number))



def add_posts(some_posts):
    global current_post_number
    sleep(1)

    first_posts.append_rows(some_posts)
    with open("current.txt", "r+") as f:
        current_post_number = int(f.read())
        current_post_number += len(some_posts)
    with open("current.txt", "w") as f:
        f.write(str(current_post_number))

    cell = second_channels.find(some_posts[0][1])
    value = third_channels.cell(cell.row, cell.col + 1).value

    new = ",".join([str(i) for i in range(current_post_number - len(some_posts) + 1, current_post_number + 1)])
    if value:
        new_value = value + new
    else:
        new_value = new

    fourth_channels.update_cell(cell.row, cell.col + 1, new_value)


def get_all_channels() -> set:
    sleep(1)
    return set(first_channels.col_values(1))
