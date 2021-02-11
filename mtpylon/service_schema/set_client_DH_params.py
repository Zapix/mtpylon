# -*- coding: utf-8 -*-
from ..utils import int128
from .constructors import Set_client_DH_params_answer, DHGenOk


async def set_client_DH_params(
        nonce: int128,
        server_nonce: int128,
        encrypted_data: bytes
) -> Set_client_DH_params_answer:
    return DHGenOk(
        nonce=nonce,
        server_nonce=server_nonce,
        new_nonce_hash1=int128(1)
    )
