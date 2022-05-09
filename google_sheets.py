import gspread
from time import sleep

TABLE = "Database"

first_account = gspread.service_account("first.json")
first_table = first_account.open(TABLE)

first_posts = first_table.worksheet("posts")
first_channels = first_table.worksheet("channels")
first_titles = first_table.worksheet("person")


second_account = gspread.service_account("second.json")
second_table = second_account.open(TABLE)

second_posts = second_table.worksheet("posts")
second_channels = second_table.worksheet("channels")
second_titles = second_table.worksheet("person")


third_account = gspread.service_account("third.json")
third_table = third_account.open(TABLE)

third_posts = third_table.worksheet("posts")
third_channels = third_table.worksheet("channels")
third_titles = third_table.worksheet("person")


fourth_account = gspread.service_account("fourth.json")
fourth_table = fourth_account.open(TABLE)

fourth_posts = fourth_table.worksheet("posts")
fourth_channels = fourth_table.worksheet("channels")
fourth_titles = fourth_table.worksheet("person")


channels_list = [first_channels, second_channels, third_channels, fourth_channels]
channel_cnt = 0


def get_idle_channels_account():
    global channel_cnt

    channel_cnt += 1
    channel_cnt %= 4

    sleep(0.26)

    return channels_list[channel_cnt]


posts_list = [first_posts, second_posts, third_posts, fourth_posts]
posts_cnt = 0


def get_idle_post_account():
    global posts_cnt

    posts_cnt += 1
    posts_cnt %= 4

    sleep(0.26)

    return posts_list[posts_cnt]


titles_list = [first_titles, second_titles, third_titles, fourth_titles]
titles_cnt = 0


def get_idle_titles_account():
    global titles_cnt

    titles_cnt += 1
    titles_cnt %= 4

    sleep(0.26)

    return titles_list[titles_cnt]


with open("current.txt", "w") as f:
    f.write(str(len(first_posts.col_values(1))))


def add_post(post, channel, channel_link, channel_id, title, date, unix) -> None:
    sleep(1)
    try:
        get_idle_post_account().append_row([post, channel, channel_link, channel_id, title, date, unix])

        with open("current.txt", "r+") as f:
            current_post_number = int(f.read())
            current_post_number += 1
        with open("current.txt", "w") as f:
            f.write(str(current_post_number))

        cell = get_idle_channels_account().find(channel)
        value = get_idle_channels_account().cell(cell.row, cell.col + 1).value

        get_idle_channels_account().update_cell(cell.row, cell.col + 1,
                                                value + "," + str(current_post_number) if value else str(
                                                    current_post_number))
    except gspread.exceptions.APIError:
        print("gspread.exceptions.APIError")
        sleep(31)
    except Exception as e:
        print(e)


def add_posts(some_posts):
    sleep(1)
    try:
        get_idle_post_account().append_rows(some_posts)
        with open("current.txt", "r+") as f:
            current_post_number = int(f.read())
            current_post_number += len(some_posts)
        with open("current.txt", "w") as f:
            f.write(str(current_post_number))

        cell = get_idle_channels_account().find(some_posts[0][1])
        value = get_idle_channels_account().cell(cell.row, cell.col + 1).value

        new = ",".join([str(i) for i in range(current_post_number - len(some_posts) + 1, current_post_number + 1)])
        if value:
            new_value = value + ',' + new
        else:
            new_value = new

        get_idle_channels_account().update_cell(cell.row, cell.col + 1, new_value)
    except gspread.exceptions.APIError:
        print("gspread.exceptions.APIError")
        sleep(31)
    except Exception as e:
        print(e)


def get_all_channels() -> set:
    try:
        return set(get_idle_channels_account().col_values(1))
    except gspread.exceptions.APIError:
        print("gspread.exceptions.APIError")
        sleep(31)
    except Exception as e:
        print(e)


def get_all_titles() -> list:
    try:
        return get_idle_titles_account().col_values(3)
    except gspread.exceptions.APIError:
        print("gspread.exceptions.APIError")
        sleep(31)
    except Exception as e:
        print(e)


def add_channel(channel):
    try:
        get_idle_channels_account().append_row([channel])
    except gspread.exceptions.APIError:
        print("gspread.exceptions.APIError")
        sleep(31)
    except Exception as e:
        print(e)
