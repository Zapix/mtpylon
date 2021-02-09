# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from .utils import long, int128
from .schema import Schema


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


service_schema = Schema(
    constructors=[
        ResPQ,
    ],
    functions=[]
)
