# -*- coding: utf-8 -*-
from typing import List, Callable, TypeVar

from .int import dump as dump_int, load as load_int
from .loaded import LoadedValue


VECTOR_ID = 0x1cb5c415


T = TypeVar('T')


def dump(
        dump_item: Callable[[T], bytes],
        vector: List[T],
        bare: bool = False
) -> bytes:
    """
    Dumps telegram vector. telegram vector starts with constructor id
    0x1cb5c415 then follows length of vector as 32-bit integer and then
    element one by one

    Args:
        dump_item - function to dump vectors item
        vector - list of items that should be dumped
    """
    dumped_items: bytes = b''.join([dump_item(item) for item in vector])
    dumped_size: bytes = dump_int(len(vector))
    dumped_constructor: bytes = dump_int(VECTOR_ID) if not bare else b''

    return dumped_constructor + dumped_size + dumped_items


def load(
        load_item: Callable[[bytes], LoadedValue[T]],
        input: bytes,
        bare: bool = False
) -> LoadedValue[List[T]]:
    """
    Loads telegram vector. with load_item function.
    checks that current value is vector and starts with 0x1cb5c415
    then read size of vector(next int value). then read all items one by one

    Args:
        load_item - function to load item from bytes
        input - bytes to load them
    """
    bare_offset = 0 if bare else 4
    if not bare and load_int(input[:4]).value != VECTOR_ID:
        raise ValueError('Wrong vector constructor')

    offset = bare_offset + 4

    loaded_size = load_int(input[bare_offset:offset])

    size = loaded_size.value

    results = []

    for _ in range(size):
        loaded_item = load_item(input[offset:])
        results.append(loaded_item.value)
        offset += loaded_item.offset

    return LoadedValue(results, offset)
