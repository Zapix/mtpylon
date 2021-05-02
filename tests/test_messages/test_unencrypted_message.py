# -*- coding: utf-8 -*-
import pytest

from mtpylon.messages.unencrypted_message import (
    unpack_message,
    pack_message,
)
from mtpylon.messages import UnencryptedMessage
from mtpylon import long, int128
from mtpylon.service_schema.functions import req_pq
from mtpylon.service_schema.constructors import ResPQ
from mtpylon.serialization.schema import CallableFunc


encoded_req_pq_message = (
    b'\x00\x00\x00\x00\x00\x00\x00\x00' +
    b'\x4a\x96\x70\x27\xc4\x7a\xe5\x51' +
    b'\x14\x00\x00\x00' +
    b'\x78\x97\x46\x60' +
    b'\x3e\x05\x49\x82\x8c\xca\x27\xe9\x66\xb3\x01\xa4\x8f\xec\xe2\xfc'
)

req_pq_message = UnencryptedMessage(
    message_id=long(0x51e57ac42770964a),
    message_data=CallableFunc(
        func=req_pq,
        params={
            'nonce': int128(0xfce2ec8fa401b366e927ca8c8249053e),
        },
    ),
)

encoded_res_pq = (
    b'\x00\x00\x00\x00\x00\x00\x00\x00' +
    b'\x01\x84\x67\xb9\xf4\x1d\x42\x60' +
    b'\x40\x00\x00\x00' +
    b'\x63\x24\x16\x05' +
    b'\xb4\xbd\x9d\x5f\xd2\x98\x4f\x16\x04\x14\x4e\x16\x77\xd7\xce\x88' +
    b'\x35\x5b\xea\x59\x40\xcc\x59\x3e\x7e\xc4\xc0\xbf\xc1\x23\x3d\x86' +
    b'\x08\x13\x54\x65\x62\x4e\x61\x25\xfd\x00\x00\x00' +
    b'\x15\xc4\xb5\x1c' +
    b'\x01\x00\x00\x00' +
    b'\x21\x6b\xe8\x6c\x02\x2b\xb4\xc3'
)

res_pq_message = UnencryptedMessage(
    message_id=long(0x60421df4b9678401),
    message_data=ResPQ(
        nonce=int128(0x88ced777164e1404164f98d25f9dbdb4),
        server_nonce=int128(0x863d23c1bfc0c47e3e59cc4059ea5b35),
        pq=b'\x13\x54\x65\x62\x4e\x61\x25\xfd',
        server_public_key_fingerprints=[
            long(0xc3b42b026ce86b21),
        ],
    ),
)


message_tests = [
    pytest.param(
        encoded_req_pq_message,
        req_pq_message,
        id='req_pq'
    ),
    pytest.param(
        encoded_res_pq,
        res_pq_message,
        id='ResPQ'
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'encoded_message,expected_message',
    message_tests
)
async def test_unpack(encoded_message, expected_message):
    message = await unpack_message(encoded_message)

    assert message == expected_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'encoded_message,message',
    message_tests
)
async def test_pack(encoded_message, message):
    encoded = await pack_message(message)

    assert encoded == encoded_message
