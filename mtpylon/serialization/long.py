# -*- coding: utf-8 -*-
from .loaded import LoadedValue
from .. import long


def dump(value: long) -> bytes:
    """
    Dumps int value as result with long
    int value is a 64 bit value in little endian order

    Args:
        value - int value that should be dumped
    """
    return value.to_bytes(8, 'little')


def load(input: bytes) -> LoadedValue[long]:
    """
    Loads long value and return it with offset.
    int value is a 64 bit value in little endian order

    Args:
        input - bytes that should be read to load int

    Raises:
        ValueError - if there aren't enough bytes

    """
    if len(input) < 8:
        raise ValueError(f'To load long required 8 bytes. Got {len(input)}')
    return LoadedValue(long(int.from_bytes(input[:8], 'little')), 8)
