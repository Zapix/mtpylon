# -*- coding: utf-8 -*-
from hashlib import sha1
from typing import Tuple
from random import getrandbits

from mtpylon import int128, int256
from mtpylon.crypto import KeyIvPair

from mtpylon.crypto.random_prime import random_prime
from mtpylon.contextvars import p_var, q_var, pq_var, dh_prime_generator
from mtpylon.utils import dump_integer_big_endian


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


def generate_tmp_key_iv(server_nonce: int128, new_nonce: int256) -> KeyIvPair:
    server_nonce_bytes = dump_integer_big_endian(server_nonce)
    new_nonce_bytes = dump_integer_big_endian(new_nonce)
    new_server_hash = sha1(new_nonce_bytes + server_nonce_bytes).digest()
    server_new_hash = sha1(server_nonce_bytes + new_nonce_bytes).digest()

    key = new_server_hash + server_new_hash[:12]
    iv = server_new_hash[12:] + new_server_hash + new_nonce_bytes[:4]

    return KeyIvPair(key=key, iv=iv)
