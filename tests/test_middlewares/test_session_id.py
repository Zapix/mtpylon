# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock

import pytest

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from mtpylon.constants import SESSION_SUBJECT_RESOURCE_NAME
from mtpylon.contextvars import (
    income_message_var,
    session_id_var,
    auth_key_var
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


@pytest.fixture
def auth_key():
    auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
    return AuthKey(auth_key_data)


@pytest.mark.asyncio
async def test_create_session_id(auth_key):
    auth_key_var.set(auth_key)

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
        session_id=session_id,
        auth_key=auth_key
    )
    assert awaited_arg == expected_event

    assert session_id_var.get() == session_id


@pytest.mark.asyncio
async def test_session_id_created_before(auth_key):
    auth_key_var.set(auth_key)

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

    await session_subject.create_session(auth_key, session_id)

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
