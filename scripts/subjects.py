from .utils import unique_by_key


def get_uniq_subjects(schedule):
    return unique_by_key(
        (lesson['subject'] for lesson in schedule),
        key_fn=lambda x: x
    )