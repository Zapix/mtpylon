# -*- coding: utf-8 -*-
from .loaded import LoadedValue


def dump(value: bytes) -> bytes:
    """
    Assume that object is bytes that has been dumped by other schema
    so just return this bytes
    """
    return value


def load(input: bytes) -> LoadedValue[bytes]:
    """
    Assume that object input will be loaded by other schema so just wrap
    it with with offset. Offset is length of input bytes
    """
    return LoadedValue(value=input, offset=len(input))
