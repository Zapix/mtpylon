# -*- coding: utf-8 -*-
from mtpylon import add


def test_correct():
    assert 4 == add(2, 2)


def test_incorrect():
    assert 4 != add(2, 3)
