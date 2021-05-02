# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.simpleschema import schema, set_task, Task

from mtpylon import long
from mtpylon.serialization import CallableFunc
from mtpylon.message_handler import MessageHandler
from mtpylon.exceptions import InvalidMessageError, InvalidServerSalt
from mtpylon.messages import UnencryptedMessage
from mtpylon.service_schema.constructors import (
    BadMessageNotification,
    BadServerSalt
)
from mtpylon.contextvars import message_id_var


@pytest.mark.asyncio
async def test_unpack_message_correct():
    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)

    unpack_message = AsyncMock(
        return_value=UnencryptedMessage(
            message_id=msg_id,
            message_data=CallableFunc(
                func=set_task,
                params={'content': 'hello world'}
            )
        )
    )

    with patch('mtpylon.message_handler.unpack_message', unpack_message):
        handler = MessageHandler(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            message_sender=message_sender
        )

        await handler.handle(request, b'obfuscated message')

        assert obfuscator.decrypt.called
        assert transport_wrapper.unwrap.called
        unpack_message.assert_awaited()

        message_sender.send_message.assert_awaited()
        task = message_sender.send_message.await_args[0][0]
        assert isinstance(task, Task)
        assert task.id == 1
        assert task.content == 'hello world'
        assert message_id_var.get() == msg_id


@pytest.mark.asyncio
async def test_invalid_message_id():
    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)

    unpack_message = AsyncMock(
        return_value=UnencryptedMessage(
            message_id=msg_id,
            message_data=CallableFunc(
                func=set_task,
                params={'content': 'hello world'}
            )
        )
    )

    validate_message = MagicMock(side_effect=InvalidMessageError(
        error_code=64
    ))

    with patch('mtpylon.message_handler.unpack_message', unpack_message):
        handler = MessageHandler(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            message_sender=message_sender,
        )

        with patch.object(handler, 'validate_message', validate_message):

            await handler.handle(request, b'obfuscated message')

            assert obfuscator.decrypt.called
            assert transport_wrapper.unwrap.called
            unpack_message.assert_awaited()

            message_sender.send_message.assert_awaited()
            error = message_sender.send_message.await_args[0][0]
            assert isinstance(error, BadMessageNotification)
            assert error.bad_msg_id == msg_id
            assert error.bad_msg_seqno == 0
            assert error.error_code == 64


@pytest.mark.asyncio
async def test_invalid_server_salt():
    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)

    unpack_message = AsyncMock(
        return_value=UnencryptedMessage(
            message_id=msg_id,
            message_data=CallableFunc(
                func=set_task,
                params={'content': 'hello world'}
            )
        )
    )

    validate_message = MagicMock(side_effect=InvalidServerSalt(
        error_code=48,
        new_server_salt=long(0xacab1312)
    ))

    with patch('mtpylon.message_handler.unpack_message', unpack_message):
        handler = MessageHandler(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            message_sender=message_sender
        )

        with patch.object(handler, 'validate_message', validate_message):
            await handler.handle(request, b'obfuscated message')

            assert obfuscator.decrypt.called
            assert transport_wrapper.unwrap.called
            unpack_message.assert_awaited()

            message_sender.send_message.assert_awaited()
            error = message_sender.send_message.await_args[0][0]
            assert isinstance(error, BadServerSalt)
            assert error.bad_msg_id == msg_id
            assert error.bad_msg_seqno == 0
            assert error.error_code == 48
            assert error.new_server_salt == long(0xacab1312)


@pytest.mark.asyncio
async def test_pass_middlewares():

    async def simple_middleware(handler, request, **params):
        return await handler(request, **params)

    middleware1 = AsyncMock(side_effect=simple_middleware)
    middleware2 = AsyncMock(side_effect=simple_middleware)

    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)

    unpack_message = AsyncMock(
        return_value=UnencryptedMessage(
            message_id=msg_id,
            message_data=CallableFunc(
                func=set_task,
                params={'content': 'hello world'}
            )
        )
    )

    with patch('mtpylon.message_handler.unpack_message', unpack_message):
        handler = MessageHandler(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            message_sender=message_sender,
            middlewares=[middleware1, middleware2],
        )

        await handler.handle(request, b'obfuscated message')

    middleware1.assert_awaited()
    middleware2.assert_awaited()
