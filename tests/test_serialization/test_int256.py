# -*- coding: utf-8 -*-
import pytest
from mtpylon.serialization.int256 import load, dump

number = 0x3E0549828CCA27E966B301A48FECE2FC3E0549828CCA27E966B301A48FECE2FC


dumped = (
    b'\xfc\xe2\xec\x8f\xa4\x01\xb3\x66\xe9\x27\xca\x8c\x82\x49\x05\x3e' +
    b'\xfc\xe2\xec\x8f\xa4\x01\xb3\x66\xe9\x27\xca\x8c\x82\x49\x05\x3e'
)


def test_dump_success():
    assert dump(number) == dumped


def test_load_success():
    loaded = load(dumped)

    assert loaded.value == number
    assert loaded.offset == 32


def test_load_error():
    with pytest.raises(ValueError):
        load(b'\x13\x00\x00')
