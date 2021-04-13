# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import int128, int256


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
