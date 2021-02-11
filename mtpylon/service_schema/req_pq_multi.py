# -*- coding: utf-8 -*-
from .constructors import ResPQ
from ..utils import long, int128


async def req_pq_multi(nonce: int128) -> ResPQ:
    """
    Just declared function to init key exchange
    """
    return ResPQ(
        nonce=nonce,
        server_nonce=int128(3),
        pq=b'here will be pq value',
        server_public_key_fingerprints=[long(4), long(5)]
    )
