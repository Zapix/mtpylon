# -*- coding: utf-8 -*-
from .loaded import LoadedValue
from .. import int256


def dump(value: int256) -> bytes:
    """
    Dumps int value as result with long
    int value is a 256  bit value in little endian order

    Args:
        value - int value that should be dumped
    """
    return value.to_bytes(32, 'little')


def load(input: bytes) -> LoadedValue[int256]:
    """
    Loads long value and return it with offset.
    int value is a 256 bit value in little endian order

    Args:
        input - bytes that should be read to load int

    Raises:
        ValueError - if there aren't enough bytes

    """
    if len(input) < 32:
        raise ValueError(f'To load long required 32 bytes. Got {len(input)}')
    return LoadedValue(int256(int.from_bytes(input[:32], 'little')), 32)
