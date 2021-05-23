# -*- coding: utf-8 -*-
import pytest

from mtpylon.serialization.vector import load, dump
from mtpylon.serialization.int import load as load_int, dump as dump_int
from mtpylon.serialization.string import (
    load as load_string,
    dump as dump_string
)


def test_dump_int():
    value = [2, 3, 4]
    dumped = (
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x02\x00\x00\x00' +  # 2
        b'\x03\x00\x00\x00' +  # 3
        b'\x04\x00\x00\x00'    # 4
    )
    assert dump(dump_int, value) == dumped


def test_dump_strings():
    value = [
        'hello',
        'world',
        'telegram'
    ]
    dumped = (
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x05' + b'hello' + b'\x00\x00' +
        b'\x05' + b'world' + b'\x00\x00' +
        b'\x08' + b'telegram' + b'\x00\x00\x00'
    )
    assert dump(dump_string, value) == dumped


def test_load_int():
    value = [2, 3, 4]
    dumped = (
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x02\x00\x00\x00' +  # 2
        b'\x03\x00\x00\x00' +  # 3
        b'\x04\x00\x00\x00'    # 4
    )

    loaded = load(load_int, dumped)

    assert loaded.value == value
    assert loaded.offset == 20


def test_load_string():
    value = [
        'hello',
        'world',
        'telegram'
    ]
    dumped = (
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x05' + b'hello' + b'\x00\x00' +
        b'\x05' + b'world' + b'\x00\x00' +
        b'\x08' + b'telegram' + b'\x00\x00\x00'
    )

    loaded = load(load_string, dumped)

    assert loaded.value == value
    assert loaded.offset == 36


def test_wrong_vector_id():
    dumped = (
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x05' + b'hello' +
        b'\x05' + b'world' +
        b'\x08' + b'telegram'
    )

    with pytest.raises(ValueError):
        load(load_int, dumped)


def test_no_length():
    dumped = (
        b'\x15\xc4\xb5\x1c'  # vector id
    )

    with pytest.raises(ValueError):
        load(load_int, dumped)


def test_dump_bare_vector():
    value = [
        'hello',
        'world',
        'telegram'
    ]

    dumped = (
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x05hello\x00\x00' +
        b'\x05world\x00\x00' +
        b'\x08telegram\x00\x00\x00'
    )

    assert dump(dump_string, value, bare=True) == dumped


def test_load_bare_vector():
    value = [
        'hello',
        'world',
        'telegram'
    ]

    dumped = (
        b'\x03\x00\x00\x00' +  # size of vector
        b'\x05hello\x00\x00' +
        b'\x05world\x00\x00' +
        b'\x08telegram\x00\x00\x00'
    )

    loaded = load(load_string, dumped, bare=True)

    assert loaded.value == value
    assert loaded.offset == 32
