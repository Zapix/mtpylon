# -*- coding: utf-8 -*-
import datetime
from typing import Generator, Optional

from mtpylon.types import long
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


def message_ids() -> Generator[long, Optional[bool], None]:
    """
    Generates server message id. Message id monotonically increases.
    Server message identifiers modulo 4 yield 1 if the message
    is a response to a client message, and 3 otherwise.
    """
    current_id = 0

    while True:
        response_msg = yield long(current_id)
        previous_id = current_id

        current_timestamp = int(datetime.datetime.now().timestamp())

        prefix = 1 if response_msg else 3
        current_id = current_timestamp - (current_timestamp % 4) + prefix

        while current_id <= previous_id:
            current_id += 4
