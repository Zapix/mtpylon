# -*- coding: utf-8 -*-
from typing import Set
from asyncio import Lock

from mtpylon.types import long
from .session_storage_protocol import SessionStorageProtocol


class InMemorySessionStorage(SessionStorageProtocol):
    """
    Stores available session in session set
    """

    def __init__(self):
        self._storage: Set[long] = set()
        self._lock = Lock()

    async def create_session(self, session_id: long):
        async with self._lock:
            self._storage.add(session_id)

    async def has_session(self, session_id: long) -> bool:
        return session_id in self._storage

    async def destroy_session(self, session_id: long):
        if session_id in self._storage:
            async with self._lock:
                self._storage.remove(session_id)
