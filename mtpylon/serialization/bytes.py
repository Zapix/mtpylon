# -*- coding: utf-8 -*-
from .loaded import LoadedValue


LONG_STRING_CHAR = b'\xfe'


def get_padded_bytes_count(length: int) -> int:
    return (4 - (length % 4)) % 4


def get_padded_bytes(length: int) -> bytes:
    padded_count = get_padded_bytes_count(length)
    return b'\x00' * padded_count


def dump(value: bytes) -> bytes:
    """
    Dumps bytes to tl string. Tl string builds by rules:
    * If L <= 253, the serialization contains one byte with the value of L,
      then L bytes of the string followed by 0 to 3 characters containing 0,
      such that the overall length of the value be divisible by 4,
      whereupon all of this is interpreted as a sequence of
      int(L/4)+1 32-bit little-endian integers.
    * If L >= 254, the serialization contains byte 254,
      followed by 3 bytes with the string length L in little-endian order,
      followed by L bytes of the string, further followed by 0 to 3 null
      padding bytes.

    Args:
        value - original bytes
    """
    prefix = b''
    if len(value) <= 253:
        size = len(value).to_bytes(1, 'little')
        tail = get_padded_bytes(len(value) + 1)
    else:
        prefix = LONG_STRING_CHAR
        size = len(value).to_bytes(3, 'little')
        tail = get_padded_bytes(len(value))

    return prefix + size + value + tail


def load(input: bytes) -> LoadedValue[bytes]:
    """
    Loads bytes from tl serialized string by rules:
    * If L <= 253, the serialization contains one byte with the value of L,
      then L bytes of the string followed by 0 to 3 characters containing 0,
      such that the overall length of the value be divisible by 4,
      whereupon all of this is interpreted as a sequence of
      int(L/4)+1 32-bit little-endian integers.
    * If L >= 254, the serialization contains byte 254,
      followed by 3 bytes with the string length L in little-endian order,
      followed by L bytes of the string, further followed by 0 to 3 null
      padding bytes.

    Args:
        input - tl serialized bytes
    """
    if len(input) == 0:
        raise ValueError('Bites string should not been empty')

    if input[:1] == LONG_STRING_CHAR:
        size = int.from_bytes(input[1:4], 'little')
        value = input[4:size + 4]
        offset = 4 + size + get_padded_bytes_count(size)
    else:
        size = int.from_bytes(input[:1], 'little')
        value = input[1: size + 1]
        offset = 1 + size + get_padded_bytes_count(size + 1)

    return LoadedValue(value, offset)
