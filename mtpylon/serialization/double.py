# -*- coding: utf-8 -*-
import struct

from .loaded import LoadedValue
from .. import double


def dump(value: double) -> bytes:
    return struct.pack('=d', value)


def load(input: bytes) -> LoadedValue[double]:
    return LoadedValue(
        double(struct.unpack('d', input[:8])[0]),
        8
    )
