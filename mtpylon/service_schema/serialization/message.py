# -*- coding: utf-8 -*-
from mtpylon.serialization.schema import LoadFunction, DumpFunction
from mtpylon.serialization.loaded import LoadedValue
from mtpylon.serialization.int import dump as dump_int, load as load_int
from mtpylon.serialization.long import dump as dump_long, load as load_long

from ..service_schema import service_schema
from ..constructors.message import Message


def dump(value: Message, dump_object: DumpFunction) -> bytes:
    data = service_schema[Message]
    dumped_body = dump_object(value.body)

    return (
        dump_int(data.id) +
        dump_long(value.msg_id) +
        dump_int(value.seqno) +
        dump_int(len(dumped_body)) +
        dumped_body
    )


def load(input: bytes, load_object: LoadFunction) -> LoadedValue[Message]:
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
