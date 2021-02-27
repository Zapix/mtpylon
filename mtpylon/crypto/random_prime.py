# -*- coding: utf-8 -*-
import random


def random_odd(n_bits: int) -> int:
    """
    Generates random odd number in range [2 ^ (n_bits - 1), 2 ^ (n_bits) - 1]
    Odd number probably is prime number
    """
    assert n_bits > 0
    value = random.getrandbits(n_bits)
    value |= (1 << n_bits) | 1
    return value
