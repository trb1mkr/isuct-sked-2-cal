import sys, requests
from bs4 import BeautifulSoup
from .constants import URL_TEACHERS


def add_teachers_full_names(schedule):
    print("Загружаем список преподавателей ИГХТУ и ищем полные ФИО...")
    
    short_names = list(get_uniq_teachers_names(schedule))
    full_names = find_teachers_full_names(fetch_teachers_info())
    names_dict = match_teachers_names(short_names, full_names)

    for lesson in schedule:
        for i, teacher in enumerate(lesson['teachers']):
            lesson['teachers'][i] = {
                'name': teacher['name'],
                'full_name': names_dict[teacher['name']]}
    
    print("ФИО преподавателей успешно загружены и сопоставлены")
    return schedule


def get_uniq_teachers_names(schedule):
    teachers = set()
    for lesson in schedule:
        for teacher in lesson['teachers']:
            teachers.add(teacher['name'])
    return teachers


def get_uniq_teachers(schedule):
    teachers = list()
    for lesson in schedule:
        for teacher in lesson['teachers']:
            if not any(teacher['name'] == curr_teacher.get("name") for curr_teacher in teachers):
                teachers.append(teacher)
    return teachers


def fetch_teachers_info():
    url = URL_TEACHERS
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


def find_teachers_full_names(teachers_info):
    soup = BeautifulSoup(teachers_info, 'html.parser')
    fio_tags = soup.find_all('td', itemprop='fio')
    return [tag.text for tag in fio_tags]


def match_teachers_names(short_names, full_names):
    teachers = {}
    for teacher in short_names:
        first_name = teacher.split()[0]
        found = False
        for full_name in full_names:
            if first_name == full_name.split()[0]:
                teachers[teacher] = full_name
                found = True
                break
        if not found:
            teachers[teacher] = teacher
    return teachers