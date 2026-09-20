import re, sys, requests
from .constants import URL_SCHEDULE


def get_schedule(group):
    print("Загружаем расписание ИГХТУ и ищем вашу группу...")
    return get_group_schedule(fetch_university_schedule(), group)


def fetch_university_schedule():
    url = URL_SCHEDULE
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("Ошибка: загруженный JSON пуст")
            sys.exit(1)
        
        print("Расписание успешно загружено")
        return data
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        sys.exit(1)


def get_group_schedule(schedule, group):
    for faculty in schedule['faculties']:
        for grp in faculty['groups']:
            if re.sub("[^0-9]", "", grp['name']) == re.sub("[^0-9]", "", group):
                return grp['lessons']
    raise ValueError(f"Группа {group} не найдена в расписании")
