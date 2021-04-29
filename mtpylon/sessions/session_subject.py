# -*- coding: utf-8 -*-
from asyncio import gather
from typing import Callable

from mtpylon.types import long
from .session_subject_protocol import SessionSubjectProtocol
from .session_storage_protocol import SessionStorageProtocol
from .session_oberver_protocol import SessionObserverProtocol
from .session_event import SessionEvent


class SessionSubject(SessionSubjectProtocol):

    def __init__(
        self,
        session_storage_factory: Callable[[], SessionStorageProtocol]
    ):
        self.session_storage = session_storage_factory()
        self.observers = []

    def subscribe(self, observer: SessionObserverProtocol):
        self.observers.append(observer)

    def unsubscribe(self, observer: SessionObserverProtocol):
        self.observers.remove(observer)

    async def _notify(self, event: SessionEvent):
        await gather(*[
            observer.update(event)
            for observer in self.observers
        ])

    async def create_session(self, session_id: long):
        await self.session_storage.create_session(session_id)
        event = SessionEvent(
            type='created',
            session_id=session_id
        )
        await self._notify(event)

    async def has_session(self, session_id: long) -> bool:
        return await self.session_storage.has_session(session_id)

    async def destroy_session(self, session_id: long):
        if await self.session_storage.has_session(session_id):
            await self.session_storage.destroy_session(session_id)
            event = SessionEvent(
                type='destroyed',
                session_id=session_id
            )
            await self._notify(event)
