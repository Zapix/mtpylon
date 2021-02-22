# -*- coding: utf-8 -*-
from mtpylon.serialization.object import load, dump


def test_dump():
    dumped_data = b'dumped data'
    assert dump(dumped_data) == dumped_data


def test_load():
    dumped_data = b'dumped data'
    loaded = load(dumped_data)

    assert loaded.value == dumped_data
    assert loaded.offset == len(dumped_data)
