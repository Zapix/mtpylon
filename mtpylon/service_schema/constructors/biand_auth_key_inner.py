# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long


@dataclass
class BindAuthKeyInner:
    nonce: long
    temp_auth_key_id: long
    perm_auth_key_id: long
    temp_session_id: long
    expires_at: int

    class Meta:
        name = 'bind_auth_key_inner'
        order = (
            'nonce',
            'temp_auth_key_id',
            'perm_auth_key_id',
            'temp_session_id',
            'expires_at',
        )
