# -*- coding: utf-8 -*-
import pytest
from mtpylon.serialization.long import load, dump


def test_dump_success():
    assert dump(275) == b'\x13\x01\x00\x00\x00\x00\x00\x00'


def test_load_success():
    loaded = load(b'\x13\x01\x00\x00\x00\x00\x00\x00')

    assert loaded.value == 275
    assert loaded.offset == 8


def test_load_error():
    with pytest.raises(ValueError):
        load(b'\x13\x00\x00')
