# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock

import pytest

from mtpylon.types import long
from mtpylon.sessions import (
    SessionEvent,
    SessionSubject,
    InMemorySessionStorage
)


@pytest.fixture
def session_subject():
    return SessionSubject(lambda: InMemorySessionStorage())


@pytest.mark.asyncio
async def test_create_session(session_subject):
    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    session_id = long(123123)

    await session_subject.create_session(session_id)

    created_event = SessionEvent(
        type='created',
        session_id=session_id,
    )

    observer1.update.assert_awaited()
    assert observer1.update.await_args[0][0] == created_event

    observer2.update.assert_awaited()
    assert observer2.update.await_args[0][0] == created_event


@pytest.mark.asyncio
async def test_destroy_session(session_subject):
    session_id = long(123123)
    await session_subject.create_session(session_id)

    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())
    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    await session_subject.destroy_session(session_id)

    destroyed_event = SessionEvent(
        type='destroyed',
        session_id=session_id,
    )

    observer1.update.assert_awaited()
    assert observer1.update.await_args[0][0] == destroyed_event

    observer2.update.assert_awaited()
    assert observer2.update.await_args[0][0] == destroyed_event


@pytest.mark.asyncio
async def test_destory_session_no_session(session_subject):
    session_id = long(123123)

    observer1 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    await session_subject.destroy_session(session_id)

    observer1.assert_not_called()


@pytest.mark.asyncio
async def test_unsubscribe_observer(session_subject):
    session1_id = long(123123)
    session2_id = long(234234)

    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    await session_subject.create_session(session1_id)

    session_subject.unsubscribe(observer1)

    await session_subject.create_session(session2_id)

    assert observer1.update.await_count == 1
    assert observer2.update.await_count == 2


@pytest.mark.asyncio
async def test_has_got_session(session_subject):
    session_id = long(123123)

    await session_subject.create_session(session_id)

    assert await session_subject.has_session(session_id)
