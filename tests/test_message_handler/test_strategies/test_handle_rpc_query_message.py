# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from mtpylon import long
from mtpylon.messages import EncryptedMessage
from mtpylon.serialization import CallableFunc
from mtpylon.message_handler.strategies.handle_rpc_query_message import (
    handle_rpc_query_message,
    run_rpc_query
)
from mtpylon.service_schema.constructors import RpcResult, RpcError, Message
from mtpylon.contextvars import server_salt_var, session_id_var

from tests.simpleschema import get_task, set_task, Task

msg_id = long(0x51e57ac42770964a)
server_salt = long(16009147158398906513)
session_id = long(11520911270507767959)


@pytest.mark.asyncio
async def test_handle_rpc_query_create_task():
    request = MagicMock()
    sender = MagicMock(send_encrypted_message=AsyncMock())

    message = EncryptedMessage(
        message_id=msg_id,
        session_id=session_id,
        salt=server_salt,
        seq_no=0,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    create_task = MagicMock()

    with patch(
        'mtpylon.message_handler.strategies.handle_rpc_query_message.create_task',  # noqa
        create_task
    ):
        await handle_rpc_query_message([], sender, request, message)

    create_task.assert_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            EncryptedMessage(
                message_id=msg_id,
                session_id=session_id,
                salt=server_salt,
                seq_no=0,
                message_data=CallableFunc(
                    func=set_task,
                    params={'content': 'hello world'}
                )
            ),
            id='encrypted message'
        ),
        pytest.param(
            Message(
                msg_id=msg_id,
                seqno=9,
                bytes=16,
                body=CallableFunc(
                    func=set_task,
                    params={'content': 'hello world'}
                )
            ),
            id='message constructor'
        ),
    ]
)
async def test_run_rpc_query_success(message):
    request = MagicMock()
    sender = MagicMock(send_encrypted_message=AsyncMock())

    server_salt_var.set(server_salt)
    session_id_var.set(session_id)

    await run_rpc_query([], sender, request, message)

    sender.send_encrypted_message.assert_awaited()

    args = sender.send_encrypted_message.await_args[0]

    server_salt_encrypt = args[1]
    assert server_salt_encrypt == server_salt

    rpc_result = args[3]

    assert isinstance(rpc_result, RpcResult)
    assert rpc_result.req_msg_id == msg_id

    task = rpc_result.result
    assert isinstance(task, Task)
    assert task.content == 'hello world'
    assert task.id == 1


@pytest.mark.asyncio
async def test_run_rpc_query_error():
    request = MagicMock()
    sender = MagicMock(send_encrypted_message=AsyncMock())

    message = EncryptedMessage(
        message_id=msg_id,
        session_id=session_id,
        salt=server_salt,
        seq_no=0,
        message_data=CallableFunc(
            func=get_task,
            params={'task_id': 4},
        )
    )

    server_salt_var.set(server_salt)
    session_id_var.set(session_id)

    await run_rpc_query([], sender, request, message)

    sender.send_encrypted_message.assert_awaited()

    args = sender.send_encrypted_message.await_args[0]
    rpc_result = args[3]

    assert isinstance(rpc_result, RpcResult)
    assert rpc_result.req_msg_id == msg_id

    error = rpc_result.result

    assert isinstance(error, RpcError)
    assert error.error_code == 404


@pytest.mark.asyncio
async def test_run_rpc_unexpected_error():
    request = MagicMock()
    sender = MagicMock(send_encrypted_message=AsyncMock())

    message = EncryptedMessage(
        message_id=msg_id,
        session_id=session_id,
        salt=server_salt,
        seq_no=0,
        message_data=CallableFunc(
            func=get_task,
            params={'task_id': 3},
        )
    )

    server_salt_var.set(server_salt)
    session_id_var.set(session_id)

    await run_rpc_query([], sender, request, message)

    sender.send_encrypted_message.assert_awaited()

    args = sender.send_encrypted_message.await_args[0]
    rpc_result = args[3]

    assert isinstance(rpc_result, RpcResult)
    assert rpc_result.req_msg_id == msg_id

    error = rpc_result.result

    assert isinstance(error, RpcError)
    assert error.error_code == 0
