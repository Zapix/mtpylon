# -*- coding: utf-8 -*-
from mtpylon import double
from mtpylon.serialization.double import load, dump


def test_dump():
    assert dump(double(1.23)) == b'\xaeG\xe1z\x14\xae\xf3?'


def test_load():
    loaded = load(b'\xaeG\xe1z\x14\xae\xf3?')

    assert abs(loaded.value - 1.23) < 0.001
    assert loaded.offset == 8
