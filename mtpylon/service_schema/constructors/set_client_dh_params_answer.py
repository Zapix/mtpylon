# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import int128


@dataclass
class DHGenOk:
    nonce: int128
    server_nonce: int128
    new_nonce_hash1: int128

    class Meta:
        name = 'dh_gen_ok'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash1'
        )


@dataclass
class DHGenRetry:
    nonce: int128
    server_nonce: int128
    new_nonce_hash2: int128

    class Meta:
        name = 'dh_gen_retry'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash2'
        )


@dataclass
class DHGenFail:
    nonce: int128
    server_nonce: int128
    new_nonce_hash3: int128

    class Meta:
        name = 'dh_gen_fail'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash3'
        )


Set_client_DH_params_answer = Annotated[
    Union[
        DHGenOk,
        DHGenRetry,
        DHGenFail
    ],
    'Set_client_DH_params_answer'
]
