from typing import Callable, Iterable, TypeVar

T = TypeVar('T')
K = TypeVar('K')


def unique_by_key(items: Iterable[T], key_fn: Callable[[T], K]) -> list[T]:
    seen = set()
    result = []
    for item in items:
        key = key_fn(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result