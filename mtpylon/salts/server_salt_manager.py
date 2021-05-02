# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Iterable
from collections import defaultdict
from asyncio import Lock
from datetime import datetime, timedelta

from mtpylon.types import long
from mtpylon.crypto import AuthKey

from .salt import Salt
from .server_salt_manager_protocol import ServerSaltManagerProtocol

SaltDict = Dict[long, Salt]
AuthSaltDict = Dict[AuthKey, SaltDict]


class ServerSaltManager(ServerSaltManagerProtocol):
    """
    Inmemory server salt manager protocol.
    """

    def __init__(self):
        self._storage: AuthSaltDict = defaultdict(dict)
        self._storage_locks = defaultdict(Lock)

    async def has_salt(self, auth_key: AuthKey, salt: long) -> bool:
        async with self._storage_locks[auth_key]:
            salts = self._storage[auth_key]

            if salt in salts:
                current_salt = salts[salt]
                now = datetime.now()

                return current_salt.since < now < current_salt.until

        return False

    async def set_salt(self, auth_key: AuthKey, salt: Salt):
        async with self._storage_locks[auth_key]:
            self._storage[auth_key][salt.salt] = salt

    async def get_future_salts(self, auth_key: AuthKey, count=1) -> List:
        count = max(1, count)
        count = min(count, 64)

        now = datetime.now()

        future_salts = [
            salt
            for salt in self._storage[auth_key].values()
            if now < salt.since < salt.until
        ]

        extra_salts_count = max(0, count - len(future_salts))

        max_valid = max(
            now - timedelta(hours=1),
            now,
            *[salt.until for salt in future_salts]
        )

        extra_salts = [
            Salt(
                since=max_valid + timedelta(days=i),
                until=max_valid + timedelta(days=i + 1)
            )
            for i in range(extra_salts_count)
        ]

        for salt in extra_salts:
            await self.set_salt(auth_key, salt)

        return future_salts[:count] + extra_salts

    async def clear(self, auth_key: Optional[AuthKey] = None):
        auth_keys: Iterable[AuthKey] = []

        if auth_key is not None:
            auth_keys = [auth_key]
        else:
            auth_keys = self._storage.keys()

        now = datetime.now()

        for key in auth_keys:
            async with self._storage_locks[key]:
                salts_to_remove = [
                    salt
                    for salt in self._storage[key].values()
                    if salt.until < now
                ]

                for salt in salts_to_remove:
                    del self._storage[key][salt.salt]
