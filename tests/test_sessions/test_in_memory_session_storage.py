# -*- coding: utf-8 -*-
import pytest

from mtpylon import long
from mtpylon.sessions import InMemorySessionStorage


@pytest.fixture
def session_storage():
    return InMemorySessionStorage()


@pytest.mark.asyncio
async def test_create_session(session_storage):
    session_id = long(123123)

    await session_storage.create_session(session_id)

    assert len(session_storage._storage) == 1
    assert session_id in session_storage._storage


@pytest.mark.asyncio
async def test_has_not_got_session(session_storage):
    session_id = long(123123)

    assert not await session_storage.has_session(session_id)


@pytest.mark.asyncio
async def test_has_got_session(session_storage):
    session_id = long(123123)

    await session_storage.create_session(session_id)

    assert await session_storage.has_session(session_id)


@pytest.mark.asyncio
async def test_destroy_session(session_storage):
    session_id = long(123123)

    await session_storage.create_session(session_id)

    await session_storage.destroy_session(session_id)

    assert not await session_storage.has_session(session_id)


@pytest.mark.asyncio
async def test_destroy_session_no_id(session_storage):
    session_id = long(123123)

    await session_storage.destroy_session(session_id)

    assert not await session_storage.has_session(session_id)
