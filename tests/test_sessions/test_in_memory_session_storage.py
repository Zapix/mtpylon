# -*- coding: utf-8 -*-
import pytest

from mtpylon import long
from mtpylon.crypto import AuthKey
from mtpylon.sessions import InMemorySessionStorage


@pytest.fixture
def session_storage():
    return InMemorySessionStorage()


@pytest.fixture
def auth_key():
    auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
    return AuthKey(auth_key_data)


@pytest.mark.asyncio
async def test_create_session(session_storage, auth_key):
    session_id = long(123123)

    await session_storage.create_session(auth_key, session_id)

    assert len(session_storage._storage) == 1


@pytest.mark.asyncio
async def test_has_not_got_session(session_storage, auth_key):
    session_id = long(123123)

    assert not await session_storage.has_session(auth_key, session_id)


@pytest.mark.asyncio
async def test_has_got_session(session_storage, auth_key):
    session_id = long(123123)

    await session_storage.create_session(auth_key, session_id)

    assert await session_storage.has_session(auth_key, session_id)


@pytest.mark.asyncio
async def test_destroy_session(session_storage, auth_key):
    session_id = long(123123)

    await session_storage.create_session(auth_key, session_id)

    await session_storage.destroy_session(auth_key, session_id)

    assert not await session_storage.has_session(auth_key, session_id)


@pytest.mark.asyncio
async def test_destroy_session_no_id(session_storage, auth_key):
    session_id = long(123123)

    await session_storage.destroy_session(auth_key, session_id)

    assert not await session_storage.has_session(auth_key, session_id)
