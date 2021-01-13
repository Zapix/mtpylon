# -*- coding: utf-8 -*-
from .loaded import LoadedValue


def dump(value: int) -> bytes:
    """
    Dumps int value as result with long
    int value is a 32 bit value in little endian order

    Args:
        value - int value that should be dumped
    """
    return value.to_bytes(4, 'little')


def load(input: bytes) -> LoadedValue[int]:
    """
    Load int value and return it with offset.
    int value is a 32 bit value in little endian order

    Args:
        input - bytes that should be read to load int

    Raises:
        ValueError - if there aren't enough bytes

    """
    if len(input) < 4:
        raise ValueError(f'To load int required 4 bytes. Got {len(input)}')
    return LoadedValue(int.from_bytes(input[:4], 'little'), 4)
