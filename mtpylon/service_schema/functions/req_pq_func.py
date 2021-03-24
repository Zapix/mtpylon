# -*- coding: utf-8 -*-
from random import getrandbits, choices

from mtpylon.utils import int128, bytes_needed
from mtpylon.contextvars import rsa_manager, server_nonce

from ..constructors import ResPQ
from ..utils import generates_pq, set_pq_context


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

    p, q = generates_pq()
    set_pq_context(p, q)

    pq = p * q

    pq_bytes = pq.to_bytes(
        bytes_needed(pq),
        'big'
    )

    manager = rsa_manager.get()

    return ResPQ(
        nonce=nonce,
        server_nonce=server_nonce_value,
        pq=pq_bytes,
        server_public_key_fingerprints=choices(manager.fingerprint_list, k=1)
    )
