# -*- coding: utf-8 -*-
from ..utils import int128, long
from .constructors import Server_DH_Params, ServerDHParamsOk


async def req_DH_params(
        nonce: int128,
        server_nonce: int128,
        p: bytes,
        q: bytes,
        public_key_fingerprint: long,
        encrypted_data: bytes
) -> Server_DH_Params:
    return ServerDHParamsOk(
        nonce=nonce,
        server_nonce=server_nonce,
        encrypted_answer=encrypted_data
    )
