from .schema import Schema


def add(a: int, b: int) -> int:
    return a + b


__all__ = [
    'Schema',
    'add',
]
