# -*- coding: utf-8 -*-
from typing import Literal
from hashlib import sha256

from .key_iv_pair import KeyIvPair
from .auth_key import AuthKey
from ..types import int128
from ..serialization.int128 import dump as dump_int128
from ..utils import dump_integer_big_endian


KeyTypes = Literal['client', 'server']


def generate_key_iv(
    auth_key: AuthKey,
    msg_key: int128,
    key_type: KeyTypes = 'server'
) -> KeyIvPair:
    x = 8 if key_type == 'server' else 0

    auth_key_bytes = dump_integer_big_endian(auth_key.value)

    msg_key_bytes = dump_int128(msg_key)

    a_bytes = sha256(msg_key_bytes + auth_key_bytes[x:36 + x]).digest()
    b_bytes = sha256(auth_key_bytes[40 + x:76 + x] + msg_key_bytes).digest()

    return KeyIvPair(
        key=a_bytes[:8] + b_bytes[8:24] + a_bytes[24:32],
        iv=b_bytes[:8] + a_bytes[8:24] + b_bytes[24:32]
    )
