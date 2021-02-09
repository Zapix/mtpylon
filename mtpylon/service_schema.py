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


@dataclass
class ServerDHParamsFail:
    nonce: int128
    server_nonce: int128
    new_nonce_hash: int128

    class Meta:
        name = 'server_DH_params_fail'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash'
        )


@dataclass
class ServerDHParamsOk:
    nonce: int128
    server_nonce: int128
    encrypted_answer: bytes

    class Meta:
        name = 'server_DH_params_ok'
        order = (
            'nonce',
            'server_nonce',
            'encrypted_answer'
        )


Server_DH_Params = Annotated[
    Union[ServerDHParamsFail, ServerDHParamsOk],
    'Server_DH_Params'
]


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


service_schema = Schema(
    constructors=[
        ResPQ,
        P_Q_inner_data,
        Server_DH_Params,
        Server_DH_inner_data,
    ],
    functions=[]
)
