# -*- coding: utf-8 -*-
from typing import Tuple
from random import getrandbits

from mtpylon.crypto.random_prime import random_prime
from mtpylon.contextvars import p_var, q_var, pq_var, dh_prime_generator


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


async def generate_g() -> int:
    """
    Generates base
    """
    return 3


async def generate_a() -> int:
    """
    Generates random 2048 bit number
    """
    return getrandbits(2048)


async def generate_dh_prime() -> int:
    """
    Generate dh_prime for key exchange. dh_prime is a safe prime number.
    2 ^ 2047 < dh_prime < 2 ^ 2048. (dh_prime - 1) / 2  is prime.
    """
    gen = dh_prime_generator.get()

    return await gen.asend(None)
