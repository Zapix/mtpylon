# -*- coding: utf-8 -*-
from .session_event import SessionEvent


class SessionObserverProtocol:

    async def update(self, event: SessionEvent):  # pragma: nocover
        ...
