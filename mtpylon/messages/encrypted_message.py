# -*- coding: utf-8 -*-
import asyncio
import logging
from typing import Any
from dataclasses import dataclass

from tgcrypto import ige256_decrypt  # type: ignore

from mtpylon.types import long
from mtpylon.schema import Schema
from mtpylon.crypto import (
    AuthKey,
    AuthKeyManager,
    AuthKeyDoesNotExist,
    generate_key_iv
)
from mtpylon.serialization.int import (
    load as load_int
)
from mtpylon.serialization.long import (
    load as load_long,
)
from mtpylon.serialization.int128 import (
    load as load_int128
)
from mtpylon.serialization.schema import (
    load as load_by_schema
)
from mtpylon.exceptions import AuthKeyNotFound, AuthKeyChangedException
from mtpylon.contextvars import auth_key_var
from mtpylon.service_schema import load as load_by_service_schema


logger = logging.getLogger(__name__)


@dataclass
class Message:
    salt: long
    session_id: long
    message_id: long
    seq_no: int
    message_data: Any


def load_message(schema: Schema, message_bytes: bytes) -> Any:
    """
    Tries to load with services, clients schema.

    Raises:
        ValueError - if couldn't parse message bytes
    """
    try:
        value = load_by_schema(schema, message_bytes).value
    except ValueError:
        value = load_by_service_schema(message_bytes).value

    return value


async def get_auth_key(
    auth_manager: AuthKeyManager,
    encrypted_message: bytes
) -> AuthKey:
    """
    Returns actual auth_key value

    Raises:
        AuthKeyNotFound - if auth key not found in auth_manager
        AuthKeyChangedException - if another key has been used
    """
    income_auth_key_id = int.from_bytes(encrypted_message[:8], 'big')

    try:
        auth_key = await auth_manager.get_key(income_auth_key_id)
    except AuthKeyDoesNotExist:
        raise AuthKeyNotFound

    expected_auth_key = auth_key_var.get(None)

    if expected_auth_key is None:
        auth_key_var.set(auth_key)
    elif expected_auth_key != auth_key:
        logger.error(
            f'Receive auth_key with id {auth_key.id}. ' +
            f'Expected {expected_auth_key.id}'
        )
        raise AuthKeyChangedException
    return auth_key


async def parse_message(schema: Schema, message_bytes: bytes) -> Message:
    """
    Loads message with extra header data
    """
    salt = load_long(message_bytes).value
    session_id = load_long(message_bytes[8:]).value
    message_id = load_long(message_bytes[16:]).value
    seq_no = load_int(message_bytes[24:]).value
    message_value = await asyncio.to_thread(
        load_message,
        schema,
        message_bytes[32:]
    )

    return Message(
        salt=salt,
        session_id=session_id,
        message_id=message_id,
        seq_no=seq_no,
        message_data=message_value
    )


async def unpack_message(
    auth_manager: AuthKeyManager,
    schema: Schema,
    encrypted_message: bytes
) -> Message:
    """
    Unpacks income message. Validates auth_key_id
    """
    auth_key = await get_auth_key(auth_manager, encrypted_message)

    msg_key = load_int128(encrypted_message[8:]).value

    key_pair = generate_key_iv(
        auth_key,
        msg_key,
        key_type='client'
    )

    message_bytes = ige256_decrypt(
        encrypted_message[24:],
        key_pair.key,
        key_pair.iv
    )

    return await parse_message(schema, message_bytes)


async def pack_message(
    auth_manager: AuthKeyManager,
    schema: Schema,
    message: Message,
) -> bytes:
    pass
