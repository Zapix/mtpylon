# -*- coding: utf-8 -*-
from functools import partial

from mtpylon import long, int128
from mtpylon.serialization import CallableFunc
from mtpylon.messages import EncryptedMessage, UnencryptedMessage
from mtpylon.message_handler.strategies import get_handle_strategy
from mtpylon.service_schema.functions import req_pq
from mtpylon.service_schema.constructors import (
    MessageContainer,
    Message,
    MsgsAck,
)
from mtpylon.message_handler.strategies.handle_unknown_message import (
    handle_unknown_message
)
from mtpylon.message_handler.strategies.handle_unencrypted_message import (
    handle_unencrypted_message
)
from mtpylon.message_handler.strategies.handle_rpc_query_message import (
    handle_rpc_query_message
)
from mtpylon.message_handler.strategies.handle_message_container import (
    handle_message_container
)
from mtpylon.message_handler.strategies.handle_msgs_ack_message import (
    handle_msgs_ack
)

from tests.simpleschema import set_task


def test_get_unknonwn_handler():
    msg_id = long(0x51e57ac42770964a)
    message = EncryptedMessage(
        message_id=msg_id,
        session_id=long(1),
        salt=long(2),
        seq_no=0,
        message_data='Wrong message data'
    )

    handler = get_handle_strategy(message)

    assert handler == handle_unknown_message


def test_get_unencrypted_handler():
    msg_id = long(0x51e57ac42770964a)
    message = UnencryptedMessage(
        message_id=msg_id,
        message_data=CallableFunc(
            func=req_pq,
            params={'nonce': int128(234)}
        ),
    )

    handler = get_handle_strategy(message)

    assert handler == handle_unencrypted_message


def test_get_rpc_call_handler():
    message = EncryptedMessage(
        message_id=long(0x51e57ac42770964a),
        session_id=long(1),
        salt=long(2),
        seq_no=0,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world!'}
        )
    )

    handler = get_handle_strategy(message)

    assert handler == handle_rpc_query_message


def test_get_message_container_selector():
    message = EncryptedMessage(
        message_id=long(0x51e57ac42770964a),
        session_id=long(1),
        salt=long(2),
        seq_no=0,
        message_data=MessageContainer(
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
                        func=set_task,
                        params={'content': 'hello world'}
                    )
                ),
            ]

        )
    )

    handler = get_handle_strategy(message)

    assert isinstance(handler, partial)
    assert handler.func == handle_message_container
    assert handler.args[0] == get_handle_strategy


def test_get_msgs_ack_handler():
    message = EncryptedMessage(
        message_id=long(0x5e0b700a00000000),
        session_id=long(1),
        salt=long(2),
        seq_no=0,
        message_data=MsgsAck(
            msg_ids=[
                long(0x51e57ac42770964a),
                long(0x60a4d9830000001c),
            ],
        ),
    )

    handler = get_handle_strategy(message)

    assert handler == handle_msgs_ack
