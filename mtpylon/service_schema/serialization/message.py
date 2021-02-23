# -*- coding: utf-8 -*-
from mtpylon.serialization.loaded import LoadedValue
from mtpylon.serialization.int import dump as dump_int, load as load_int
from mtpylon.serialization.long import dump as dump_long, load as load_long
from mtpylon.serialization.object import (
    dump as dump_object,
    load as load_object
)

from ..service_schema import service_schema
from ..constructors.message import Message


def dump(value: Message) -> bytes:
    data = service_schema[Message]

    return (
        dump_int(data.id) +
        dump_long(value.msg_id) +
        dump_int(value.seqno) +
        dump_int(len(value.body)) +
        dump_object(value.body)
    )


def load(input: bytes) -> LoadedValue[Message]:
    msg_id = load_long(input[4:]).value
    seqno = load_int(input[12:]).value
    bytes_count = load_int(input[16:]).value
    body = load_object(input[20:20 + bytes_count]).value

    return LoadedValue(
        value=Message(
            msg_id=msg_id,
            seqno=seqno,
            bytes=bytes_count,
            body=body
        ),
        offset=20 + bytes_count
    )
