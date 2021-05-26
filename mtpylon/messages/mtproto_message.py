# -*- coding: utf-8 -*-
from typing import cast

from mtpylon.crypto import AuthKeyManager
from mtpylon.schema import Schema

from .types import MtprotoMessage, UnencryptedMessage, EncryptedMessage
from .utils import is_unencrypted_message
from .unencrypted_message import (
    unpack_message as unpack_unencrypted,
    pack_message as pack_unencrypted,
)
from .encrypted_message import (
    unpack_message as unpack_encrypted,
    pack_message as pack_encrypted
)


async def unpack_message(
    auth_manager: AuthKeyManager,
    schema: Schema,
    value: bytes
) -> MtprotoMessage:
    if is_unencrypted_message(value):
        return await unpack_unencrypted(value)
    return await unpack_encrypted(auth_manager, schema, value)


async def pack_message(
    auth_manager: AuthKeyManager,
    schema: Schema,
    value: MtprotoMessage
) -> bytes:
    if isinstance(value, UnencryptedMessage):
        return await pack_unencrypted(value)
    value = cast(EncryptedMessage, value)
    return await pack_encrypted(schema, value)
