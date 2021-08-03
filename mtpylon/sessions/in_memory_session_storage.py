# -*- coding: utf-8 -*-
from typing import Set, Tuple
from asyncio import Lock

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from .session_storage_protocol import SessionStorageProtocol


AuthKeySessionTuple = Tuple[AuthKey, long]


class InMemorySessionStorage(SessionStorageProtocol):
    """
    Stores available session in session set
    """

    def __init__(self):
        self._storage: Set[AuthKeySessionTuple] = set()
        self._lock = Lock()

    async def create_session(self, auth_key: AuthKey, session_id: long):
        auth_key_session_tuple = (auth_key, session_id)
        async with self._lock:
            self._storage.add(auth_key_session_tuple)

    async def has_session(self, auth_key: AuthKey, session_id: long) -> bool:
        auth_key_session_tuple = (auth_key, session_id)
        return auth_key_session_tuple in self._storage

    async def destroy_session(self, auth_key: AuthKey, session_id: long):
        auth_key_session_tuple = (auth_key, session_id)
        if auth_key_session_tuple in self._storage:
            async with self._lock:
                self._storage.remove(auth_key_session_tuple)
