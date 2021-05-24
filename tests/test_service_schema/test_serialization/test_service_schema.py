# -*- coding: utf-8 -*-
import pytest

from mtpylon import long
from mtpylon.service_schema import load, dump, service_schema
from mtpylon.service_schema.constructors import (
    MsgsAck,
    Message,
    MessageContainer,
    RpcResult,
    RpcError,
)
from mtpylon.serialization import CallableFunc

from tests.echoschema import schema, Reply, echo


@pytest.fixture
def common_schema():
    return schema | service_schema


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
        MessageContainer(
            messages=[
                Message(
                    msg_id=long(0x5e0b700a00000000),
                    seqno=7,
                    bytes=20,
                    body=MsgsAck(
                        msg_ids=[
                            long(1621416313)
                        ]
                    ),
                ),
                Message(
                    msg_id=long(0x60a4d9830000001c),
                    seqno=9,
                    bytes=16,
                    body=CallableFunc(
                        func=echo,
                        params={'content': 'hello world'}
                    )
                ),
            ]
        ),
        (
            b'\xdc\xf8\xf1\x73'  # vector container combinator
            b'\x02\x00\x00\x00'  # vector size
            b'\x00\x00\x00\x00\x0a\x70\x0b\x5e'  # msg_id
            b'\x07\x00\x00\x00'  # seq No
            b'\x14\x00\x00\x00'  # meessage length
            b'\x59\xb4\xd6\x62'  # msg_ack combinator
            b'\x15\xc4\xb5\x1c'  # vector combinator
            b'\x01\x00\x00\x00'  # vector size
            b'\x79\xd9\xa4\x60\x00\x00\x00\x00'  # ack msg id
            b'\x1c\x00\x00\x00\x83\xd9\xa4\x60'  # message id
            b'\x09\x00\x00\x00'  # msg seq no
            b'\x10\x00\x00\x00'  # message length
            b'\x0a\x3b\x35\xfb'  # echo func
            b'\x0b\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64'  # content str
        ),
        id='msg_container',
    ),
    pytest.param(
        RpcResult(
            req_msg_id=long(0x5e0b700a00000000),
            result=RpcError(
                error_code=404,
                error_message='Not Found',
            ),
        ),
        (
            b'\x01m\\\xf3' +
            b'\x00\x00\x00\x00\np\x0b^' +
            b'\x19\xcaD!\x94\x01\x00\x00\tNot Found\x00\x00'
        ),
        id='rpc response error'
    ),
    pytest.param(
        RpcResult(
            req_msg_id=long(0x5e0b700a00000000),
            result=Reply(
                content='hello world',
                rand_id=44,
            ),
        ),
        (
            b'\x01m\\\xf3' +
            b'\x00\x00\x00\x00\np\x0b^' +
            b'>\x00j\r,\x00\x00\x00\x0bhello world'
        ),
        id='rpc response with users schema'
    ),
    pytest.param(
        RpcResult(
            req_msg_id=long(0x5e0b700a00000000),
            result=RpcError(
                error_code=404,
                error_message='Not Found',
            ),
        ),
        (
            b'\x01m\\\xf3' +
            b'\x00\x00\x00\x00\np\x0b^' +
            b'\x19\xcaD!\x94\x01\x00\x00\tNot Found\x00\x00'
        ),
        id='rpc response rpc error'
    ),
    pytest.param(
        RpcResult(
            req_msg_id=long(0x5e0b700a00000000),
            result=Reply(
                content='hello world',
                rand_id=44,
            ),
        ),
        (
            b'\x01m\\\xf3' +
            b'\x00\x00\x00\x00\np\x0b^' +
            b'>\x00j\r,\x00\x00\x00\x0bhello world'
        ),
        id='rpc response reply'
    ),
    pytest.param(
        Message(
            msg_id=long(0x60a4d98300000018),
            seqno=7,
            bytes=20,
            body=MsgsAck(
                msg_ids=[
                    long(1621416313)
                ]
            )
        ),
        (
            b'\x11\xe5\xb8['  # message combinator
            b'\x18\x00\x00\x00\x83\xd9\xa4\x60'  # msgId
            b'\x07\x00\x00\x00'  # seq No
            b'\x14\x00\x00\x00'  # meessage length
            b'\x59\xb4\xd6\x62'  # msg_ack combinator
            b'\x15\xc4\xb5\x1c'  # vector combinator
            b'\x01\x00\x00\x00'  # vector size
            b'\x79\xd9\xa4\x60\x00\x00\x00\x00'  # ack msg id
        ),
        id='message with msg ack'
    ),
    pytest.param(
        Message(
            msg_id=long(0x60a4d9830000001c),
            seqno=9,
            bytes=16,
            body=CallableFunc(
                func=echo,
                params={'content': 'hello world'}
            )
        ),
        (
            b'\x11\xe5\xb8['  # message combinator
            b'\x1c\x00\x00\x00\x83\xd9\xa4\x60'  # message id
            b'\x09\x00\x00\x00'  # msg seq no
            b'\x10\x00\x00\x00'  # message length
            b'\x0a\x3b\x35\xfb'  # echo func
            b'\x0b\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64'  # content str
        ),
        id='message with rpc call'
    )
]


@pytest.mark.parametrize(
    'value,dumped_value',
    test_params
)
def test_dump(common_schema, value, dumped_value):
    assert dump(value, common_schema) == dumped_value


@pytest.mark.parametrize(
    'value,dumped_value',
    test_params
)
def test_load(common_schema, value, dumped_value):
    loaded = load(dumped_value, common_schema)

    assert loaded.value == value
    assert loaded.offset == len(dumped_value)
