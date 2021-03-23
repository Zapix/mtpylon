# -*- coding: utf-8 -*-
from random import getrandbits, choices

from mtpylon.utils import long, int128, bytes_needed
from mtpylon.contextvars import rsa_manager, server_nonce, p, q, pq
from mtpylon.crypto.random_prime import random_prime

from ..constructors import ResPQ


async def req_pq(nonce: int128) -> ResPQ:
    """
    Handles DH exchange initiation.
    Generates server_nonce and store them in context var for further validation
    Generates p, q prime factors and multiply them. P, q, and pq values are
    stored in context manager too.
    Get's random fingerprint from rsa manager. Access RSA manager via
    context variable
    """
    server_nonce_value = int128(getrandbits(128))
    server_nonce.set(server_nonce_value)

    p_value = random_prime(64)
    q_value = random_prime(64)

    if q_value < p_value:
        p_value, q_value = q_value, p_value

    p.set(long(p_value))
    q.set(long(q_value))
    pq_value = p_value * q_value
    pq_bytes = pq_value.to_bytes(
        bytes_needed(pq_value),
        'big'
    )
    pq.set(pq_bytes)

    manager = rsa_manager.get()

    return ResPQ(
        nonce=nonce,
        server_nonce=server_nonce_value,
        pq=pq_bytes,
        server_public_key_fingerprints=choices(manager.fingerprint_list, k=1)
    )
