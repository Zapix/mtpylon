# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long, int128


@dataclass
class Client_DH_Inner_Data:
    nonce: int128
    server_nonce: int128
    retry_id: long
    g_b: bytes

    class Meta:
        name = 'client_DH_inner_data'
        order = (
            'nonce',
            'server_nonce',
            'retry_id',
            'g_b',
        )
