# -*- coding: utf-8 -*-
from typing import List, Any, Generator, cast
from dataclasses import dataclass, field
import logging

from aiohttp.web import WebSocketResponse, Request

from .types import long
from .constants import (
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
)
from .acknowledgement_store import (
    AcknowledgementStoreProtocol,
    AcknowledgementMessage,
)
from .messages import (
    message_ids,
    pack_message,
    UnencryptedMessage,
    EncryptedMessage,
    MtprotoMessage
)
from .transports import Obfuscator, TransportWrapper
from .schema import Schema
from .service_schema import service_schema
from .service_schema.constructors import MessageContainer, Message
from .contextvars import auth_key_var

logger = logging.getLogger(__name__)


@dataclass
class MessageSender:

    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    ws: WebSocketResponse

    _msg_ids: Generator[long, bool, None] = field(init=False)

    def __post_init__(self):
        self._msg_ids = message_ids()
        self._msg_ids.send(None)
        self._common_schema = self.schema | service_schema

    async def _send_message(self, request: Request, message: MtprotoMessage):
        if self.ws.closed:
            logger.warning('Ws connection has been closed before')
            return

        try:
            message_bytes = await pack_message(
                request.app[AUTH_KEY_MANAGER_RESOURCE_NAME],
                self._common_schema,
                message
            )
        except ValueError as e:
            logger.error(f'Can`t dump message {message} close ws connection')
            logger.error(e)
            await self.ws.close()
        else:
            wrapped_message = self.transport_wrapper.wrap(message_bytes)
            encrypted_data = self.obfuscator.encrypt(wrapped_message)
            logger.info(f'Send message with id {message.message_id}')
            await self.ws.send_bytes(encrypted_data)

    def _build_message_container(
        self,
        msg_lists: List[AcknowledgementMessage],
        message_id: long,
        message_data: Any
    ) -> MessageContainer:
        return MessageContainer(
            messages=[
                Message(
                    msg_id=msg.message_id,
                    seqno=0,
                    body=msg.data,
                )
                for msg in msg_lists
            ] + [
                Message(
                    msg_id=message_id,
                    seqno=0,
                    body=message_data,
                )
            ]
        )

    def get_msg_id(self, response: bool = False):
        return self._msg_ids.send(response)

    async def send_unencrypted_message(
        self,
        request: Request,
        data: Any,
        response: bool = False
    ):
        message = UnencryptedMessage(
            message_id=self.get_msg_id(response),
            message_data=data
        )

        await self._send_message(request, message)

    async def send_encrypted_message(
        self,
        request: Request,
        server_salt: long,
        session_id: long,
        data: Any,
        response: bool = False,
        acknowledgement_required: bool = False
    ):
        logger.debug(f'Send message: {str(data)}')

        auth_key = auth_key_var.get()
        acknowledgement_store = cast(
            AcknowledgementStoreProtocol,
            request.app[ACKNOWLEDGEMENT_STORE_RESOURCE_NAME]
        )

        message_id = self.get_msg_id(response)

        msg_list = await acknowledgement_store.get_message_list(
            auth_key,
            session_id
        )

        if len(msg_list) > 0:
            message_container = self._build_message_container(
                msg_list,
                message_id=message_id,
                message_data=data
            )
            message = EncryptedMessage(
                salt=server_salt,
                session_id=session_id,
                message_id=self.get_msg_id(),
                seq_no=0,
                message_data=message_container
            )
        else:
            message = EncryptedMessage(
                salt=server_salt,
                session_id=session_id,
                message_id=message_id,
                seq_no=0,
                message_data=data
            )

        await self._send_message(request, message)

        if acknowledgement_required:
            logger.debug(f'Set that acknowledgement required for {message_id}')
            await acknowledgement_store.set_message(
                auth_key,
                session_id,
                message_id,
                data
            )
