# -*- coding: utf-8 -*-
import asyncio
import logging
from typing import Any
from random import randbytes

from tgcrypto import ige256_decrypt, ige256_encrypt  # type: ignore

from mtpylon.schema import Schema
from mtpylon.crypto import (
    AuthKey,
    AuthKeyManager,
    AuthKeyDoesNotExist,
    generate_key_iv,
    get_msg_key,
)
from mtpylon.serialization.int import (
    load as load_int,
    dump as dump_int,
)
from mtpylon.serialization.long import (
    load as load_long,
    dump as dump_long,
)
from mtpylon.serialization.int128 import (
    load as load_int128,
    dump as dump_int128,
)
from mtpylon.serialization.schema import (
    load as load_by_schema,
    dump as dump_by_schema
)
from mtpylon.exceptions import (
    AuthKeyNotFound,
    AuthKeyChangedException,
    DumpError
)
from mtpylon.contextvars import auth_key_var
from mtpylon.service_schema import (
    load as load_by_service_schema,
    dump as dump_by_service_schema
)
from .types import EncryptedMessage


logger = logging.getLogger(__name__)


MIN_PAD = 12


def load_data(schema: Schema, message_bytes: bytes) -> Any:
    """
    Tries to load with services, clients schema.

    Raises:
        ValueError - if couldn't parse message bytes
    """
    try:
        value = load_by_schema(
            message_bytes,
            schema=schema
        ).value
    except ValueError:
        value = load_by_service_schema(
            message_bytes,
            schema=schema
        ).value

    return value


def dump_data(schema: Schema, data: Any) -> bytes:
    """
    Tries to dumps data as clients data.
    If it failed tries dump as server data

    Raises:
        DumpError - if data couldn't been dumped
    """

    try:
        dumped_data = dump_by_schema(data, schema=schema, custom_dumpers=None)
    except DumpError:
        dumped_data = dump_by_service_schema(data, schema)

    return dumped_data


async def load_message(
    schema: Schema,
    message_bytes: bytes
) -> EncryptedMessage:
    """
    Loads message with extra header data
    """
    salt = load_long(message_bytes).value
    session_id = load_long(message_bytes[8:]).value
    message_id = load_long(message_bytes[16:]).value
    seq_no = load_int(message_bytes[24:]).value
    message_value = await asyncio.to_thread(
        load_data,
        schema,
        message_bytes[32:]
    )

    return EncryptedMessage(
        salt=salt,
        session_id=session_id,
        message_id=message_id,
        seq_no=seq_no,
        message_data=message_value
    )


async def dump_message(schema: Schema, message: EncryptedMessage) -> bytes:
    data_bytes = await asyncio.to_thread(
        dump_data,
        schema,
        message.message_data
    )
    return (
        dump_long(message.salt) +
        dump_long(message.session_id) +
        dump_long(message.message_id) +
        dump_int(message.seq_no) +
        dump_int(len(data_bytes)) +
        data_bytes
    )


def pad_bytes(raw_data):
    length_with_min_pad = len(raw_data) + MIN_PAD
    round_pad = (16 - (length_with_min_pad % 16)) % 16
    total_pad = round_pad + MIN_PAD

    return randbytes(total_pad)


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

    try:
        expected_auth_key = auth_key_var.get()
    except LookupError:
        expected_auth_key = auth_key
        auth_key_var.set(auth_key)

    if expected_auth_key != auth_key:
        logger.error(
            f'Receive auth_key with id {auth_key.id}. ' +
            f'Expected {expected_auth_key.id}'
        )
        raise AuthKeyChangedException

    return auth_key


async def unpack_message(
    auth_manager: AuthKeyManager,
    schema: Schema,
    encrypted_message: bytes
) -> EncryptedMessage:
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

    return await load_message(schema, message_bytes)


async def pack_message(
    schema: Schema,
    message: EncryptedMessage,
) -> bytes:
    dumped_message = await dump_message(schema, message)
    padded_message = dumped_message + pad_bytes(dumped_message)

    try:
        auth_key = auth_key_var.get()
    except LookupError:
        logger.error('Auth key should be set before response')
        raise ValueError('Auth key should be set before')

    msg_key = get_msg_key(auth_key, padded_message)

    key_iv_pair = generate_key_iv(auth_key, msg_key)

    encrypted_message = ige256_encrypt(
        padded_message,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    return (
        auth_key.id.to_bytes(8, 'big') +
        dump_int128(msg_key) +
        encrypted_message
    )
