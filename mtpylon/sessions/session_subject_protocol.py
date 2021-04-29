# -*- coding: utf-8 -*-
from typing import List

from .session_storage_protocol import SessionStorageProtocol
from .session_oberver_protocol import SessionObserverProtocol


class SessionSubjectProtocol(SessionStorageProtocol):

    session_storage: SessionStorageProtocol

    observers: List[SessionObserverProtocol]

    def subscribe(self, observer: SessionObserverProtocol):  # pragma: nocover
        ...

    def unsubscribe(
        self,
        observer: SessionObserverProtocol
    ):  # pragma: nocover
        ...
