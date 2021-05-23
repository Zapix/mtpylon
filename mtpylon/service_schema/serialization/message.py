# -*- coding: utf-8 -*-
from mtpylon.serialization.schema import LoadFunction, DumpFunction
from mtpylon.serialization.loaded import LoadedValue
from mtpylon.serialization.int import dump as dump_int, load as load_int
from mtpylon.serialization.long import dump as dump_long, load as load_long

from ..service_schema import service_schema
from ..constructors.message import Message


def dump(
    value: Message,
    dump_object: DumpFunction,
    bare: bool = False
) -> bytes:
    data = service_schema[Message]
    dumped_body = dump_object(value.body, bare=False)

    constructor = dump_int(data.id) if not bare else b''

    return (
        constructor +
        dump_long(value.msg_id) +
        dump_int(value.seqno) +
        dump_int(len(dumped_body)) +
        dumped_body
    )


def load(
    input: bytes,
    load_object: LoadFunction,
    bare: bool = False
) -> LoadedValue[Message]:
    offset = 4 if not bare else 0
    msg_id = load_long(input[offset:]).value
    seqno = load_int(input[offset + 8:]).value
    bytes_count = load_int(input[offset + 12:]).value
    body = load_object(
        input[offset + 16:offset + 16 + bytes_count],
        bare=False
    ).value

    return LoadedValue(
        value=Message(
            msg_id=msg_id,
            seqno=seqno,
            bytes=bytes_count,
            body=body
        ),
        offset=offset + 16 + bytes_count
    )
