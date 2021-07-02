# -*- coding: utf-8 -*-
import logging
from random import randint, getrandbits, choices

from aiohttp import web

from mtpylon.utils import bytes_needed
from mtpylon.types import int128
from mtpylon.contextvars import server_nonce_var
from mtpylon.constants import RSA_MANAGER_RESOURCE_NAME

from ..constructors import ResPQ
from ..utils import generates_pq, set_pq_context


logger = logging.getLogger('mtpylon.authorization')


async def req_pq_multi(request: web.Request, nonce: int128) -> ResPQ:
    """
    Handles DH exchange initiation.
    Generates server_nonce and store them in context var for further validation
    Generates p, q prime factors and multiply them. P, q, and pq values are
    stored in context manager too.
    Get's random fingerprint from rsa manager. Access RSA manager via
    """
    logger.info('Handle req_pq_multi')

    server_nonce_value = int128(getrandbits(128))
    logger.debug(f'server_nonce_value: {server_nonce_value}')

    server_nonce_var.set(server_nonce_value)

    p, q = generates_pq()
    set_pq_context(p, q)

    pq = p * q

    pq_bytes = pq.to_bytes(
        bytes_needed(pq),
        'big'
    )

    manager = request.app[RSA_MANAGER_RESOURCE_NAME]

    return ResPQ(
        nonce=nonce,
        server_nonce=server_nonce_value,
        pq=pq_bytes,
        server_public_key_fingerprints=choices(
            manager.fingerprint_list,
            k=randint(1, len(manager.fingerprint_list)),
        )
    )
