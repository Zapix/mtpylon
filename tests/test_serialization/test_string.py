# -*- coding: utf-8 -*-
from mtpylon.serialization.bytes import LONG_STRING_CHAR
from mtpylon.serialization.string import load, dump


def test_dump_short_string():
    value = 'My Hello World!'
    dumped = b'\x0f' + value.encode()

    assert dump(value) == dumped


def test_dump_with_offset():
    value = 'Hello World!'
    dumped = b'\x0c' + value.encode() + b'\x00\x00\x00'

    assert dump(value) == dumped


def test_dump_long_string():
    value = 'asdfg' * 101
    size_bytes = len(value).to_bytes(3, 'little')
    dumped = LONG_STRING_CHAR + size_bytes + value.encode() + b'\x00' * 3

    assert dump(value) == dumped


def test_load_short_string():
    value = 'My Hello World!'
    dumped = b'\x0f' + value.encode()

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 16


def test_load_with_offset():
    value = 'Hello World!'
    dumped = b'\x0c' + value.encode() + b'\x00\x00\x00'

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 16


def test_load_long_string():
    value = 'asdfg' * 101
    size_bytes = len(value).to_bytes(3, 'little')
    dumped = LONG_STRING_CHAR + size_bytes + value.encode() + b'\x00' * 3

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 512
