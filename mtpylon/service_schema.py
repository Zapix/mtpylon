# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Annotated, Union

from .utils import long, int128, int256
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


@dataclass
class PQInnerData:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256

    class Meta:
        name = 'p_q_inner_data'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce'
        )


@dataclass
class PQInnerDataDC:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    dc: int

    class Meta:
        name = 'p_q_inner_data_dc'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'dc'
        )


@dataclass
class PQInnerDataTemp:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    expires_in: int

    class Meta:
        name = 'p_q_inner_data_temp'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'expires_in',
        )


@dataclass
class PQInnerDataTempDC:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    expires_in: int
    dc: int

    class Meta:
        name = 'p_q_inner_data_temp_dc'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'dc',
            'expires_in',
        )


P_Q_inner_data = Annotated[
    Union[
        PQInnerData,
        PQInnerDataDC,
        PQInnerDataTemp,
        PQInnerDataTempDC,
    ],
    'P_Q_inner_data'
]


service_schema = Schema(
    constructors=[
        ResPQ,
        P_Q_inner_data,
    ],
    functions=[]
)
