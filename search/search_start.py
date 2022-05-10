from search import search_for_channel
from google_sheets import get_all_titles, get_idle_titles_account

cached_titles = get_all_titles()
cached_titles = [[cached_titles[i], i] for i in range(len(cached_titles))]

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
