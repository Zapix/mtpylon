# -*- coding: utf-8 -*-
import pytest

from mtpylon.serialization.bytes import load, dump


def test_dump_short_string():
    value = b'\x01\x02\x03\x04'
    dumped = b'\x04\x01\x02\x03\x04\x00\x00\x00'

    assert dump(value) == dumped


def test_dump_short_13_string():
    value = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d'
    dumped = (
        b'\x0d\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x00\x00'
    )

    assert dump(value) == dumped


def test_dump_long_string_length_256():
    value = b''.join([(x % 256).to_bytes(1, 'little') for x in range(256)])
    dumped = b'\xfe\x00\x01\x00' + value

    assert dump(value) == dumped


def test_dump_long_string_length_257():
    value = b''.join([(x % 256).to_bytes(1, 'little') for x in range(257)])
    dumped = b'\xfe\x01\x01\x00' + value + b'\x00\x00\x00'

    assert dump(value) == dumped


def test_load_short_string():
    value = b'\x01\x02\x03\x04'
    dumped = b'\x04\x01\x02\x03\x04\x00\x00\x00'

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 8


def test_load_short_13_string():
    value = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d'
    dumped = (
        b'\x0d\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x00\x00'
    )

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 16


def test_load_long_string_256():
    value = b''.join([(x % 256).to_bytes(1, 'little') for x in range(256)])
    dumped = b'\xfe\x00\x01\x00' + value

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 260


def test_load_long_string_257():
    value = b''.join([(x % 256).to_bytes(1, 'little') for x in range(257)])
    dumped = b'\xfe\x01\x01\x00' + value + b'\x00\x00\x00'

    loaded = load(dumped)

    assert loaded.value == value
    assert loaded.offset == 264


def test_load_value_error():
    with pytest.raises(ValueError):
        load(b'')
