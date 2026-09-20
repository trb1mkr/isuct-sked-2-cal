from .utils import unique_by_key


def get_uniq_audiences(schedule):
    return unique_by_key(
        ({"name": audience['name'], "subject": lesson['subject']}
         for lesson in schedule for audience in lesson['audiences']),
        key_fn=lambda a: (a['name'], a['subject'])
    )