import re
import requests
from bs4 import BeautifulSoup
from .constants import URL_TEACHERS
from .utils import unique_by_key
from .exceptions import TeachersFetchError


def add_teachers_full_names(schedule):
    print("Загружаем список преподавателей ИГХТУ и ищем полные ФИО...")
    
    short_names = get_uniq_teacher_names(schedule)
    full_names = find_teachers_full_names(fetch_teachers_info())
    names_dict = match_teachers_names(short_names, full_names)

    for lesson in schedule:
        for i, teacher in enumerate(lesson['teachers']):
            lesson['teachers'][i] = {
                'name': teacher['name'],
                'full_name': names_dict[teacher['name']]}
    
    print("ФИО преподавателей успешно загружены и сопоставлены")
    return schedule


def get_uniq_teacher_names(schedule):
    return unique_by_key(
        (teacher['name'] for lesson in schedule for teacher in lesson['teachers']),
        key_fn=lambda x: x
    )


def get_uniq_teachers(schedule):
    return unique_by_key(
        (teacher for lesson in schedule for teacher in lesson['teachers']),
        key_fn=lambda t: t['name']
    )


def fetch_teachers_info():
    url = URL_TEACHERS
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
        
    except requests.exceptions.HTTPError as e:
        raise TeachersFetchError(f"HTTP ошибка: {e}") from e
    except requests.exceptions.RequestException as e:
        raise TeachersFetchError(f"Ошибка запроса: {e}") from e


def find_teachers_full_names(teachers_info):
    soup = BeautifulSoup(teachers_info, 'html.parser')
    fio_tags = soup.find_all('td', itemprop='fio')
    if fio_tags:
        return [tag.text for tag in fio_tags]
    # Fallback: extract from raw HTML
    return re.findall(r'[А-Я][а-я]{2,}\s+[А-Я][а-я]+\s+[А-Я][а-я]+', teachers_info)


def _normalize_schedule_name(name):
    parts = re.split(r'[\s.]+', name)
    parts = [p for p in parts if p]
    if len(parts) >= 3:
        return (parts[0] + parts[1][0] + parts[2][0]).upper()
    elif len(parts) == 2:
        return (parts[0] + parts[1][0]).upper()
    return name.upper()


def _normalize_website_name(name):
    parts = name.split()
    if len(parts) >= 3:
        return (parts[0] + parts[1][0] + parts[2][0]).upper()
    elif len(parts) == 2:
        return (parts[0] + parts[1][0]).upper()
    return name.upper()


def match_teachers_names(short_names, full_names):
    short_norm = {_normalize_schedule_name(n): n for n in short_names}
    full_norm = {_normalize_website_name(n): n for n in full_names}

    teachers = {}
    for norm, short in short_norm.items():
        if norm in full_norm:
            teachers[short] = full_norm[norm]
        else:
            teachers[short] = short
    return teachers