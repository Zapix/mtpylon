# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import int128


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
