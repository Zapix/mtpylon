# -*- coding: utf-8 -*-
from typing import Any, Generator
from dataclasses import dataclass, field
import logging

from aiohttp.web import WebSocketResponse, Request

from .types import long
from .messages import (
    message_ids,
    pack_message,
    UnencryptedMessage,
    Message,
    MtprotoMessage
)
from .transports import Obfuscator, TransportWrapper
from .schema import Schema
from .service_schema import service_schema

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
                request.app['auth_key_manager'],
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

    def get_msg_id(self, response: bool):
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
        response: bool = False
    ):
        logger.debug(f'Send message: {str(data)}')
        message = Message(
            salt=server_salt,
            session_id=session_id,
            message_id=self.get_msg_id(response),
            seq_no=0,
            message_data=data
        )

        await self._send_message(request, message)
