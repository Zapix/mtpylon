# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import int128


@dataclass
class Server_DH_inner_data:
    nonce: int128
    server_nonce: int128
    g: int
    dh_prime: bytes
    g_a: bytes
    server_time: int

    class Meta:
        name = 'server_DH_inner_data'
        order = (
            'nonce',
            'server_nonce',
            'g',
            'dh_prime',
            'g_a',
            'server_time'
        )
