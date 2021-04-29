# -*- coding: utf-8 -*-
from typing import Protocol

from mtpylon import long


class SessionStorageProtocol(Protocol):

    async def create_session(self, session_id: long):  # pragma: nocover
        """
        Saves info about new session(session_id)
        """
        ...

    async def has_session(self, session_id: long) -> bool:  # pragma: nocover
        """
        Checks has session_id been stored or not
        """
        ...

    async def destroy_session(self, session_id: long):  # pragma: nocover
        """
        Removes info about stored
        """
        ...
