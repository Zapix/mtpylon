# -*- coding: utf-8 -*-
from .loaded import LoadedValue
from .. import int128


def dump(value: int128) -> bytes:
    """
    Dumps int value as result with long
    int value is a 128 bit value in little endian order

    Args:
        value - int value that should be dumped
    """
    return value.to_bytes(16, 'little')


def load(input: bytes) -> LoadedValue[int128]:
    """
    Loads long value and return it with offset.
    int value is a 128 bit value in little endian order

    Args:
        input - bytes that should be read to load int

    Raises:
        ValueError - if there aren't enough bytes

    """
    if len(input) < 16:
        raise ValueError(f'To load long required 16 bytes. Got {len(input)}')
    return LoadedValue(int128(int.from_bytes(input[:16], 'little')), 16)
