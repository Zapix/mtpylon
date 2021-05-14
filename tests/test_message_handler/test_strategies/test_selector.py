# -*- coding: utf-8 -*-
from mtpylon import long, int128
from mtpylon.serialization import CallableFunc
from mtpylon.messages import Message, UnencryptedMessage
from mtpylon.message_handler.strategies import get_handle_strategy
from mtpylon.service_schema.functions import req_pq
from mtpylon.message_handler.strategies.handle_unknown_message import (
    handle_unknown_message
)
from mtpylon.message_handler.strategies.handle_unencrypted_message import (
    handle_unencrypted_message
)
from mtpylon.message_handler.strategies.handle_rpc_query_message import (
    handle_rpc_query_message
)

from tests.simpleschema import set_task


def test_get_unknonwn_handler():
    msg_id = long(0x51e57ac42770964a)
    message = Message(
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
    message = Message(
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
