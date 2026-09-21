import os
from scripts import schedule, teachers, excel, calendar, exceptions


def make_schedule_file():
    my_schedule = None
    while True:
        group = input("Введите номер группы: ")
        try:
            my_schedule = schedule.get_schedule(group)
            break
        except exceptions.GroupNotFoundError as e:
            print(e)
        except (exceptions.ScheduleFetchError, exceptions.ScheduleParseError) as e:
            print(f"Ошибка загрузки расписания: {e}")
            return

    try:
        my_schedule = teachers.add_teachers_full_names(my_schedule)
    except exceptions.TeachersFetchError as e:
        print(f"Ошибка загрузки преподавателей: {e}")
        return

    try:
        excel.create_workbook(my_schedule)
    except exceptions.ExcelGenerationError as e:
        print(f"Ошибка создания Excel: {e}")
        return


def make_calendar():
    print("Переходим к созданию календаря")
    input("Откройте документ, прочитайте инструкцию и отредактируйте получившийся документ\n" \
    "P.S. ОБЯЗАТЕЛЬНО внестите ЛЮБОЕ изменение в документ\n" \
    "P.P.S Без этого Excel не кэширует значения вычисляемых ячеек и программа не сможет их считать на следующем шаге\n" \
    "Нажмите Enter (КАК ТОЛЬКО ВЫПОЛНИЛИ ТО, ЧТО ОПИСАНО ВЫШЕ)")
    try:
        calendar.create_calendar()
    except exceptions.CalendarGenerationError as e:
        print(f"Ошибка создания календаря: {e}")
        return


output_dir_existed = os.path.exists('output')
if not output_dir_existed:
    print("Папки output не было - создаём")
    os.mkdir('output')

download = input("Загрузить расписание? (n, если расписание загружено и вы хотите перейти к созданию календаря) (Y/n): ").strip().lower()
if download == '' or download == 'y' or not output_dir_existed:
    make_schedule_file()
make_calendar()