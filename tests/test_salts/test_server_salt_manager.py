# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from mtpylon.salts import Salt, ServerSaltManager


@pytest.mark.asyncio
async def test_server_salt_not_found():
    salt_manager = ServerSaltManager()

    salt_value = long(12312)

    auth_key = AuthKey(123123)

    assert not await salt_manager.has_salt(auth_key, salt_value)


@pytest.mark.asyncio
async def test_set_server_salt():
    salt_manager = ServerSaltManager()

    salt_value = long(12312)
    now = datetime.now()
    since = now - timedelta(hours=12)
    until = now + timedelta(hours=12)
    salt = Salt(salt=salt_value, since=since, until=until)

    auth_key = AuthKey(123123)

    assert not await salt_manager.has_salt(auth_key, salt_value)

    await salt_manager.set_salt(auth_key, salt)

    assert await salt_manager.has_salt(auth_key, salt_value)


@pytest.mark.asyncio
async def test_server_salt_ohter_auth_key():
    salt_manager = ServerSaltManager()

    salt_value = long(12312)
    now = datetime.now()
    since = now - timedelta(hours=12)
    until = now + timedelta(hours=12)
    salt = Salt(salt=salt_value, since=since, until=until)

    auth_key = AuthKey(123123)
    other_key = AuthKey(232323)

    await salt_manager.set_salt(auth_key, salt)

    assert await salt_manager.has_salt(auth_key, salt_value)
    assert not await salt_manager.has_salt(other_key, salt_value)


@pytest.mark.asyncio
async def test_server_salt_expired():
    salt_manager = ServerSaltManager()

    salt_value = long(12312)
    now = datetime.now()
    since = now - timedelta(hours=36)
    until = now - timedelta(hours=12)
    salt = Salt(salt=salt_value, since=since, until=until)

    auth_key = AuthKey(123123)

    await salt_manager.set_salt(auth_key, salt)
    assert not await salt_manager.has_salt(auth_key, salt_value)


@pytest.mark.asyncio
async def test_get_future_salts():
    salt_manager = ServerSaltManager()

    now = datetime.now()
    salts = [
        Salt(
            since=now - timedelta(hours=12) + timedelta(days=i),
            until=now + timedelta(hours=12) + timedelta(days=i),
        )
        for i in range(4)
    ]

    auth_key = AuthKey(123123)

    for salt in salts:
        await salt_manager.set_salt(auth_key, salt)

    future_salts = await salt_manager.get_future_salts(auth_key, 7)

    assert len(future_salts) == 7

    for salt in salts[1:]:
        assert salt in future_salts


@pytest.mark.asyncio
async def test_get_future_salts_max_value():
    salt_manager = ServerSaltManager()

    now = datetime.now()
    salts = [
        Salt(
            since=now - timedelta(hours=12) + timedelta(days=i),
            until=now + timedelta(hours=12) + timedelta(days=i),
        )
        for i in range(4)
    ]

    auth_key = AuthKey(123123)

    for salt in salts:
        await salt_manager.set_salt(auth_key, salt)

    future_salts = await salt_manager.get_future_salts(auth_key, 128)

    assert len(future_salts) == 64

    for salt in salts[1:]:
        assert salt in future_salts


@pytest.mark.asyncio
async def test_get_future_salts_negative():
    salt_manager = ServerSaltManager()

    now = datetime.now()
    salts = [
        Salt(
            since=now - timedelta(hours=12) + timedelta(days=i),
            until=now + timedelta(hours=12) + timedelta(days=i),
        )
        for i in range(4)
    ]

    auth_key = AuthKey(123123)

    for salt in salts:
        await salt_manager.set_salt(auth_key, salt)

    future_salts = await salt_manager.get_future_salts(auth_key, -3)

    assert len(future_salts) == 1

    future_salt = future_salts[0]

    assert future_salt in salts


@pytest.mark.asyncio
async def test_clear_specific_auth_key():
    salt_manager = ServerSaltManager()

    auth_key = AuthKey(123123)

    now = datetime.now()
    salts = [
        Salt(
            since=now - timedelta(hours=36) - timedelta(days=i),
            until=now - timedelta(hours=12) - timedelta(days=i),
        )
        for i in range(4)
    ]

    for salt in salts:
        await salt_manager.set_salt(auth_key, salt)

    await salt_manager.clear(auth_key)
    assert len(salt_manager._storage[auth_key]) == 0


@pytest.mark.asyncio
async def test_clear_all_auth_keys():
    salt_manager = ServerSaltManager()

    auth_keys = [
        AuthKey(123123),
        AuthKey(224232),
    ]

    now = datetime.now()
    for auth_key in auth_keys:
        salts = [
            Salt(
                since=now - timedelta(hours=36) - timedelta(days=i),
                until=now - timedelta(hours=12) - timedelta(days=i),
            )
            for i in range(8)
        ]

        for salt in salts[:4]:
            await salt_manager.set_salt(auth_key, salt)

    await salt_manager.clear()

    for auth_key in auth_keys:
        assert len(salt_manager._storage[auth_key]) == 0
