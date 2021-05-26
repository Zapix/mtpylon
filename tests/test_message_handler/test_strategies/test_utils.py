# -*- coding: utf-8 -*-
import pytest

from mtpylon import long, int128
from mtpylon.messages import UnencryptedMessage, EncryptedMessage
from mtpylon.serialization import CallableFunc
from mtpylon.message_handler.strategies.utils import (
    is_unencrypted_message,
    is_rpc_call_message,
    is_container_message,
)
from mtpylon.service_schema.functions import req_pq, ping
from mtpylon.service_schema.constructors import (
    MsgsAck,
    MessageContainer,
    Message as MessageConstructor
)

from tests.simpleschema import set_task


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            UnencryptedMessage(
                message_id=long(0x51e57ac42770964a),
                message_data=CallableFunc(
                    func=req_pq,
                    params={'nonce': int128(234234)}
                ),
            ),
            id='unencrypted message'
        ),
    ]
)
def test_is_unencrypted_message_true(message):
    assert is_unencrypted_message(message)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            UnencryptedMessage(
                message_id=long(0x51e57ac42770964a),
                message_data='wrong data',
            ),
            id='unencrypted message wrong rpc call'
        ),
        pytest.param(
            UnencryptedMessage(
                message_id=long(0x51e57ac42770964a),
                message_data=CallableFunc(
                    func=set_task,
                    params={'content': 'hello world!'}
                ),
            ),
            id='unencrypted message wrong rpc call'
        ),
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data='Wrong message data'
            ),
            id='encrypted message'
        )
    ]
)
def test_is_unencrypted_message_false(message):
    assert not is_unencrypted_message(message)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data=CallableFunc(
                    func=set_task,
                    params={'content': 'hello world!'}
                )
            ),
            id='encrypted message'
        )
    ]
)
def test_is_rpc_call_true(message):
    assert is_rpc_call_message(message)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            UnencryptedMessage(
                message_id=long(0x51e57ac42770964a),
                message_data=CallableFunc(
                    func=req_pq,
                    params={'nonce': int128(234234)}
                ),
            ),
            id='unencrypted message'
        ),
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data='Wrong message data'
            ),
            id='encrypted message wrong data'
        ),
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data='some un expected data'
            ),
            id='encrypted message ping call'
        ),
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data=CallableFunc(
                    func=ping,
                    params={'ping_id': long(111)},
                )
            ),
            id='encrypted message ping call'
        )
    ]
)
def test_is_rpc_call_message_false(message):
    assert not is_rpc_call_message(message)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            pytest.param(
                UnencryptedMessage(
                    message_id=long(0x51e57ac42770964a),
                    message_data=CallableFunc(
                        func=req_pq,
                        params={'nonce': int128(234234)}
                    ),
                ),
                id='unencrypted message'
            ),

        ),
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data=CallableFunc(
                    func=ping,
                    params={'ping_id': long(111)},
                )
            ),
            id='encrypted message ping call'
        )
    ]
)
def test_is_not_container_message(message):
    assert not is_container_message(message)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data=MessageContainer(
                    messages=[
                        MessageConstructor(
                            msg_id=long(0x5e0b700a00000000),
                            seqno=7,
                            bytes=20,
                            body=MsgsAck(
                                msg_ids=[
                                    long(1621416313)
                                ]
                            ),
                        ),
                        MessageConstructor(
                            msg_id=long(0x60a4d9830000001c),
                            seqno=9,
                            bytes=16,
                            body=CallableFunc(
                                func=set_task,
                                params={'content': 'hello world'}
                            )
                        ),
                    ]

                )
            ),
        ),
    ]
)
def test_is_container_message(message):
    assert is_container_message(message)
