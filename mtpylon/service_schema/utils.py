# -*- coding: utf-8 -*-
from typing import Tuple

from mtpylon.crypto.random_prime import random_prime
from mtpylon.contextvars import p_var, q_var, pq_var


def generates_pq() -> Tuple[int, int]:
    """
    Generates p, q are  prime numbers. Generates them until p * q < 2 ^ 63 - 1
    """
    p, q = 0, 0

    while not 0 < p * q < (2 ** 63) - 1 and p == q:
        q = random_prime(32)
        p = random_prime(32)

    return min(p, q), max(p, q)


def set_pq_context(p: int, q: int):
    p_var.set(p)
    q_var.set(q)
    pq_var.set(p * q)
