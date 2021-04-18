# -*- coding: utf-8 -*-
import logging
from hashlib import sha1
from typing import AsyncGenerator, Tuple
from random import getrandbits

from mtpylon import int128, int256
from mtpylon.crypto import KeyIvPair
from mtpylon.serialization.int128 import dump as dump_128
from mtpylon.serialization.int256 import dump as dump_256
from mtpylon.crypto.random_prime import random_prime
from mtpylon.contextvars import p_var, q_var, pq_var


logger = logging.getLogger(__name__)


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


async def generate_dh_prime(gen: AsyncGenerator[int, None]) -> int:
    """
    Generate dh_prime for key exchange. dh_prime is a safe prime number.
    2 ^ 2047 < dh_prime < 2 ^ 2048. (dh_prime - 1) / 2  is prime.
    """

    return await gen.asend(None)


def generate_tmp_key_iv(server_nonce: int128, new_nonce: int256) -> KeyIvPair:
    server_nonce_bytes = dump_128(server_nonce)
    new_nonce_bytes = dump_256(new_nonce)

    new_nonce_server_nonce_hash = sha1(
        new_nonce_bytes + server_nonce_bytes
    ).digest()
    server_nonce_new_nonce_hash = sha1(
        server_nonce_bytes + new_nonce_bytes
    ).digest()
    new_none_new_nonce_hash = sha1(
        new_nonce_bytes + new_nonce_bytes
    ).digest()

    key = new_nonce_server_nonce_hash + server_nonce_new_nonce_hash[:12]
    iv = (
        server_nonce_new_nonce_hash[12:] +
        new_none_new_nonce_hash +
        new_nonce_bytes[:4]
    )

    logger.debug('Server nonce {:0x}'.format(
        int.from_bytes(server_nonce_bytes, 'big')
    ))
    logger.debug('New nonce {:0x}'.format(
        int.from_bytes(new_nonce_bytes, 'big')
    ))
    logger.debug('Key {:0x}'.format(int.from_bytes(key, 'big')))
    logger.debug('Iv {:0x}'.format(int.from_bytes(iv, 'big')))

    return KeyIvPair(key=key, iv=iv)
