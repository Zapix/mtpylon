# -*- coding: utf-8 -*-
from mtpylon.crypto.random_prime import random_odd


def test_random_odd():
    value = random_odd(64)

    assert value % 2 == 1
    assert value >> 64 == 1
