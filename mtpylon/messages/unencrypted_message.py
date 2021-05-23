# -*- coding: utf-8 -*-
import asyncio

from mtpylon import long
from mtpylon.service_schema import load as load_schema, dump as dump_schema
from mtpylon.serialization.int import load as load_int, dump as dump_int
from mtpylon.serialization.long import load as load_long, dump as dump_long

from .types import UnencryptedMessage


def unpack(input: bytes) -> UnencryptedMessage:
    loaded_msg_id = load_long(input[8:])
    loaded_size = load_int(input[16:])
    size = loaded_size.value
    loaded_value = load_schema(input[20:20 + size])

    return UnencryptedMessage(
        message_id=loaded_msg_id.value,
        message_data=loaded_value.value
    )


def pack(message: UnencryptedMessage):
    auth_id = dump_long(long(0))

    msg_id = dump_long(message.message_id)

    value = dump_schema(message.message_data)

    size = dump_int(len(value))

    return auth_id + msg_id + size + value


async def unpack_message(input: bytes) -> UnencryptedMessage:
    return await asyncio.to_thread(unpack, input)


async def pack_message(message: UnencryptedMessage) -> bytes:
    return await asyncio.to_thread(pack, message)
