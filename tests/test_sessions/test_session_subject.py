# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock

import pytest

from mtpylon.crypto import AuthKey
from mtpylon.types import long
from mtpylon.sessions import (
    SessionEvent,
    SessionSubject,
    InMemorySessionStorage
)


@pytest.fixture
def session_subject():
    return SessionSubject(lambda: InMemorySessionStorage())


@pytest.fixture
def auth_key():
    auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
    return AuthKey(auth_key_data)


@pytest.mark.asyncio
async def test_create_session(session_subject, auth_key):
    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    session_id = long(123123)

    await session_subject.create_session(auth_key, session_id)

    created_event = SessionEvent(
        type='created',
        session_id=session_id,
        auth_key=auth_key
    )

    observer1.update.assert_awaited()
    assert observer1.update.await_args[0][0] == created_event

    observer2.update.assert_awaited()
    assert observer2.update.await_args[0][0] == created_event


@pytest.mark.asyncio
async def test_destroy_session(session_subject, auth_key):
    session_id = long(123123)
    await session_subject.create_session(auth_key, session_id)

    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())
    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    await session_subject.destroy_session(auth_key, session_id)

    destroyed_event = SessionEvent(
        type='destroyed',
        session_id=session_id,
        auth_key=auth_key
    )

    observer1.update.assert_awaited()
    assert observer1.update.await_args[0][0] == destroyed_event

    observer2.update.assert_awaited()
    assert observer2.update.await_args[0][0] == destroyed_event


@pytest.mark.asyncio
async def test_destory_session_no_session(session_subject, auth_key):
    session_id = long(123123)

    observer1 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    await session_subject.destroy_session(auth_key, session_id)

    observer1.assert_not_called()


@pytest.mark.asyncio
async def test_unsubscribe_observer(session_subject, auth_key):
    session1_id = long(123123)
    session2_id = long(234234)

    observer1 = MagicMock(update=AsyncMock())
    observer2 = MagicMock(update=AsyncMock())

    session_subject.subscribe(observer1)
    session_subject.subscribe(observer2)

    await session_subject.create_session(auth_key, session1_id)

    session_subject.unsubscribe(observer1)

    await session_subject.create_session(auth_key, session2_id)

    assert observer1.update.await_count == 1
    assert observer2.update.await_count == 2


@pytest.mark.asyncio
async def test_has_got_session(session_subject, auth_key):
    session_id = long(123123)

    await session_subject.create_session(auth_key, session_id)

    assert await session_subject.has_session(auth_key, session_id)
