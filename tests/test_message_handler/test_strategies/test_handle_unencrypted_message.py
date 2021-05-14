# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock

import pytest

from mtpylon import long
from mtpylon.serialization import CallableFunc
from mtpylon.messages import UnencryptedMessage
from mtpylon.contextvars import income_message_var
from mtpylon.message_handler.strategies.handle_unencrypted_message import (
    handle_unencrypted_message
)


from tests.simpleschema import set_task, Task


@pytest.mark.asyncio
async def test_handle_unencrypted_message():
    msg_id = long(0x51e57ac42770964a)
    message = UnencryptedMessage(
        message_id=msg_id,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world!'}
        ),
    )

    middlewares = []

    request = MagicMock()

    sender = MagicMock(send_unencrypted_message=AsyncMock())

    await handle_unencrypted_message(
        middlewares,
        sender,
        request,
        message
    )

    sender.send_unencrypted_message.assert_awaited()

    task = sender.send_unencrypted_message.await_args[0][1]
    assert isinstance(task, Task)
    assert task.id == 1
    assert task.content == 'hello world!'

    assert income_message_var.get() == message
