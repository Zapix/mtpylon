# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock

import pytest

from mtpylon.types import long
from mtpylon.constants import SESSION_SUBJECT_RESOURCE_NAME
from mtpylon.contextvars import (
    income_message_var,
    session_id_var,
)
from mtpylon.serialization import CallableFunc
from mtpylon.messages import EncryptedMessage
from mtpylon.sessions import (
    SessionSubject,
    SessionEvent,
    InMemorySessionStorage,
)
from mtpylon.middlewares.set_session_id import set_session_id

from tests.simpleschema import set_task


@pytest.mark.asyncio
async def test_create_session_id():
    msg_id = long(0x51e57ac42770964a)
    session_id = long(123123)
    salt = long(234234)

    message = EncryptedMessage(
        salt=salt,
        session_id=session_id,
        message_id=msg_id,
        seq_no=1,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    income_message_var.set(message)

    handler = AsyncMock()

    session_subject = SessionSubject(InMemorySessionStorage)

    request = MagicMock()
    request.app = {
        SESSION_SUBJECT_RESOURCE_NAME: session_subject
    }

    session_observer = MagicMock()
    session_observer.update = AsyncMock()
    session_subject.subscribe(session_observer)

    await set_session_id(handler, request, content='hello world')

    handler.assert_awaited()
    session_observer.update.assert_awaited()

    awaited_arg = session_observer.update.await_args[0][0]
    expected_event = SessionEvent(
        type='created',
        session_id=session_id
    )
    assert awaited_arg == expected_event

    assert session_id_var.get() == session_id


@pytest.mark.asyncio
async def test_session_id_created_before():
    msg_id = long(0x51e57ac42770964a)
    session_id = long(123123)
    salt = long(234234)

    message = EncryptedMessage(
        salt=salt,
        session_id=session_id,
        message_id=msg_id,
        seq_no=1,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    income_message_var.set(message)

    handler = AsyncMock()

    session_subject = SessionSubject(InMemorySessionStorage)

    await session_subject.create_session(session_id=session_id)

    request = MagicMock()
    request.app = {
        SESSION_SUBJECT_RESOURCE_NAME: session_subject
    }

    session_observer = MagicMock()
    session_observer.update = AsyncMock()
    session_subject.subscribe(session_observer)

    await set_session_id(handler, request, content='hello world')

    handler.assert_awaited()
    session_observer.update.assert_not_awaited()

    assert session_id_var.get() == session_id
