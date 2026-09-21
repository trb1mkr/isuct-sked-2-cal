class ScheduleError(Exception):
    """Базовая ошибка расписания."""
    pass


class ScheduleFetchError(ScheduleError):
    """Ошибка загрузки расписания с удалённого источника."""
    pass


class ScheduleParseError(ScheduleError):
    """Ошибка парсинга данных расписания."""
    pass


class GroupNotFoundError(ScheduleError):
    """Указанная группа не найдена в расписании."""
    pass


class TeacherError(Exception):
    """Базовая ошибка преподавателей."""
    pass


class TeachersFetchError(TeacherError):
    """Ошибка загрузки списка преподавателей."""
    pass


class TeacherMatchError(TeacherError):
    """Ошибка сопоставления сокращённых имён с полными ФИО."""
    pass


class CalendarError(Exception):
    """Базовая ошибка календаря."""
    pass


class CalendarGenerationError(CalendarError):
    """Ошибка генерации .ics календаря."""
    pass


class ExcelError(Exception):
    """Базовая ошибка Excel."""
    pass


class ExcelTemplateError(ExcelError):
    """Ошибка шаблона Excel (файл не найден или неверная структура)."""
    pass


class ExcelGenerationError(ExcelError):
    """Ошибка создания Excel файла."""
    pass