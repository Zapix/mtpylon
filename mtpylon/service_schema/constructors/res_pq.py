# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from mtpylon.utils import int128, long


@dataclass
class ResPQ:
    nonce: int128
    server_nonce: int128
    pq: bytes
    server_public_key_fingerprints: List[long]

    class Meta:
        name = 'resPQ'
        order = (
            'nonce',
            'server_nonce',
            'pq',
            'server_public_key_fingerprints'
        )
