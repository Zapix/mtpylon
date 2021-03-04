# -*- coding: utf-8 -*-
from mtpylon.serialization.long import load as load_long


def is_unencrypted_message(buffer: bytes) -> bool:
    """
    Unencrypted message starts with auth_key_id equals 0
    See: https://core.telegram.org/mtproto/description#unencrypted-message
    """
    loaded_auth_key_id = load_long(buffer)

    return loaded_auth_key_id.value == 0


def is_encrypted_message(buffer: bytes) -> bool:
    """
    Encrypted message starts with auth_key_id that not equals to zero
    See: https://core.telegram.org/mtproto/description#encrypted-message
    """
    return not is_unencrypted_message(buffer)
