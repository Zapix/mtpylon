# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mtpylon import long
from mtpylon.serialization import CallableFunc
from mtpylon.message_handler import MessageHandler
from mtpylon.messages import UnencryptedMessage, Message
from mtpylon.contextvars import (
    income_message_var
)

from tests.simpleschema import schema, set_task, Task


@pytest.mark.asyncio
async def test_unpack_unencyprted_message_correct():
    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)

    message = UnencryptedMessage(
        message_id=msg_id,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    unpack_message = AsyncMock(return_value=message)

    with patch(
        'mtpylon.message_handler.message_handler.unpack_message',
        unpack_message
    ):
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
        task = message_sender.send_message.await_args[0][1]
        assert isinstance(task, Task)
        assert task.id == 1
        assert task.content == 'hello world'
        assert income_message_var.get() == message


@pytest.mark.asyncio
async def test_unpack_encrypted_message_correct():
    obfuscator = MagicMock()
    obfuscator.decrypt__return_value = b'decrypted data'
    transport_wrapper = MagicMock()
    transport_wrapper.unwrap__return_value = b'unwrapped data'
    message_sender = MagicMock(
        send_message=AsyncMock()
    )
    request = MagicMock()

    msg_id = long(0x51e57ac42770964a)
    session_id = long(123123)
    salt = long(234234)

    message = Message(
        salt=salt,
        session_id=session_id,
        message_id=msg_id,
        seq_no=1,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    unpack_message = AsyncMock(return_value=message)

    with patch(
        'mtpylon.message_handler.message_handler.unpack_message',
        unpack_message
    ):
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

    with patch(
        'mtpylon.message_handler.message_handler.unpack_message',
        unpack_message
    ):
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
