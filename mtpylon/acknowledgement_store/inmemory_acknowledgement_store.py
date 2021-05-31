# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Dict, Any, List

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from .acknowledgement_store_protocol import AcknowledgementStoreProtocol
from .types import AuthSessionHash, AcknowledgementMessage

MessageAcknowledgementDict = Dict[long, Any]
AuthAcknowledgementDict = Dict[AuthSessionHash, MessageAcknowledgementDict]


class InmemoryAcknowledgementStore(AcknowledgementStoreProtocol):
    """
    Stores messages that should receive acknowledgement in memory
    """

    def __init__(self):
        self._store: AuthAcknowledgementDict = defaultdict(dict)

    async def create_session_store(
        self,
        auth_key: AuthKey,
        session_id: long
    ):
        auth_session_hash = AuthSessionHash(
            auth_key,
            session_id
        )

        self._store[auth_session_hash] = {}

    async def drop_session_store(
        self,
        auth_key: AuthKey,
        session_id: long
    ):
        auth_session_hash = AuthSessionHash(
            auth_key,
            session_id
        )

        if auth_session_hash in self._store:
            del self._store[auth_session_hash]

    async def set_message(
        self,
        auth_key: AuthKey,
        session_id: long,
        message_id: long,
        data: Any
    ):
        auth_session_hash = AuthSessionHash(
            auth_key=auth_key,
            session_id=session_id
        )

        self._store[auth_session_hash][message_id] = data

    async def get_message_list(
        self,
        auth_key: AuthKey,
        session_id: long,
    ) -> List[AcknowledgementMessage]:
        auth_session_hash = AuthSessionHash(
            auth_key=auth_key,
            session_id=session_id
        )

        return [
            AcknowledgementMessage(
                message_id=msg_id,
                data=msg_data
            )
            for (msg_id, msg_data) in self._store[auth_session_hash].items()
        ]

    async def delete_message(
        self,
        auth_key: AuthKey,
        session_id: long,
        message_id: long
    ):
        auth_session_hash = AuthSessionHash(
            auth_key=auth_key,
            session_id=session_id
        )

        if message_id in self._store[auth_session_hash]:
            del self._store[auth_session_hash][message_id]
