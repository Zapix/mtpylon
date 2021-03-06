# -*- coding: utf-8 -*-
import pytest

from mtpylon import long
from mtpylon.service_schema import load, dump
from mtpylon.service_schema.constructors import (
    MsgsAck,
    Message,
    MessageContainer
)


test_params = [
    pytest.param(
        MsgsAck(
            msg_ids=[
                long(0x5e0b700a00000000),
                long(0x5e0b800e00000000),
            ]
        ),
        (
            b'\x59\xb4\xd6\x62' +
            b'\x15\xc4\xb5\x1c' +
            b'\x02\x00\x00\x00' +
            b'\x00\x00\x00\x00\x0a\x70\x0b\x5e' +
            b'\x00\x00\x00\x00\x0e\x80\x0b\x5e'
        ),
        id='msgs_ack'
    ),
    pytest.param(
        Message(
            msg_id=long(0x5e0b700a00000000),
            seqno=0,
            bytes=14,
            body=b'dumped message'
        ),
        (
            b'\x11\xe5\xb8[' +
            b'\x00\x00\x00\x00\x0a\x70\x0b\x5e' +
            b'\x00\x00\x00\x00' +
            b'\x0e\x00\x00\x00' +
            b'dumped message'
        ),
        id='message'
    ),
    pytest.param(
        MessageContainer(
            messages=[
                Message(
                    msg_id=long(0x5e0b700a00000000),
                    seqno=0,
                    bytes=14,
                    body=b'dumped message'
                ),
                Message(
                    msg_id=long(0x5e0b800e00000000),
                    seqno=0,
                    bytes=22,
                    body=b'another dumped message'
                ),
            ]
        ),
        (
            b'HI\xc3\x94' +  # msg_container number
            b'\x15\xc4\xb5\x1c' +  # vector number
            b'\x02\x00\x00\x00' +  # vector size
            b'\x11\xe5\xb8[' +  # message number
            b'\x00\x00\x00\x00\x0a\x70\x0b\x5e' +  # msg_id
            b'\x00\x00\x00\x00' +  # seqno
            b'\x0e\x00\x00\x00' +  # byte size
            b'dumped message' +  # body
            b'\x11\xe5\xb8[' +  # message number
            b'\x00\x00\x00\x00\x0e\x80\x0b\x5e' +  # msg_id
            b'\x00\x00\x00\x00' +  # seqno
            b'\x16\x00\x00\x00' +  # byte size
            b'another dumped message'  # body
        ),
        id='msg_container',
    ),
]


@pytest.mark.parametrize(
    'value,dumped_value',
    test_params
)
def test_dump(value, dumped_value):
    assert dump(value) == dumped_value


@pytest.mark.parametrize(
    'value,dumped_value',
    test_params
)
def test_load(value, dumped_value):
    loaded = load(dumped_value)

    assert loaded.value == value
    assert loaded.offset == len(dumped_value)
