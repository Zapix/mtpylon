# -*- coding: utf-8 -*-
from hashlib import sha256

from mtpylon import int128
from mtpylon.crypto import AuthKey
from mtpylon.utils import dump_integer_big_endian
from mtpylon.serialization.int128 import load as load_int128


def get_msg_key(auth_key: AuthKey, raw_data: bytes) -> int128:
    """
    :param raw_data:
    :return:
    """
    auth_key_bytes = dump_integer_big_endian(auth_key.value)[88:88 + 32]
    prepared_data = auth_key_bytes + raw_data

    loaded = load_int128(sha256(prepared_data).digest()[8:24])
    return loaded.value
