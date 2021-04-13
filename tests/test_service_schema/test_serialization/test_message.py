# -*- coding: utf-8 -*-
from mtpylon import long
from mtpylon.service_schema.constructors import Message
from mtpylon.service_schema.serialization.message import load, dump

message = Message(
    msg_id=long(32),
    seqno=0,
    bytes=14,
    body=b'dumped message'
)

dumped_message = (
    b'\x11\xe5\xb8[' +
    b'\x20\x00\x00\x00\x00\x00\x00\x00' +
    b'\x00\x00\x00\x00' +
    b'\x0e\x00\x00\x00' +
    b'dumped message'
)


def test_dump_message():
    assert dump(message) == dumped_message


def test_load_message():
    loaded = load(dumped_message + b'prefix that should be skipped')

    assert loaded.offset == len(dumped_message)
    assert loaded.value == message
