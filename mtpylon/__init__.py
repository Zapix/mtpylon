from .schema import Schema
from .utils import long, int128, int256, double


def add(a: int, b: int) -> int:
    return a + b


__all__ = [
    'Schema',
    'add',
    'long',
    'int128',
    'int256',
    'double',
]
