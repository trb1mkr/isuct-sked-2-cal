import re, requests
from .constants import URL_SCHEDULE
from .exceptions import ScheduleFetchError, ScheduleParseError, GroupNotFoundError


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
            raise ScheduleParseError("загруженный JSON пуст")
        
        print("Расписание успешно загружено")
        return data
        
    except requests.exceptions.HTTPError as e:
        raise ScheduleFetchError(f"HTTP ошибка: {e}") from e
    except requests.exceptions.RequestException as e:
        raise ScheduleFetchError(f"Ошибка запроса: {e}") from e
    except ValueError as e:
        raise ScheduleParseError(f"Ошибка при обработке JSON: {e}") from e


def get_group_schedule(schedule, group):
    for faculty in schedule['faculties']:
        for grp in faculty['groups']:
            if re.sub("[^0-9]", "", grp['name']) == re.sub("[^0-9]", "", group):
                return grp['lessons']
    raise GroupNotFoundError(f"Группа {group} не найдена в расписании")
