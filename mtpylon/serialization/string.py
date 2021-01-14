# -*- coding: utf-8 -*-
from .loaded import LoadedValue
from .bytes import load as bytes_load, dump as bytes_dump


def dump(value: str) -> bytes:
    """
    Dumps utf-8 string by tl rules
    """
    return bytes_dump(value.encode())


def load(input: bytes):
    """
    Loads utf-8 string
    """
    loaded = bytes_load(input)

    return LoadedValue(
        loaded.value.decode('utf-8'),
        loaded.offset
    )
