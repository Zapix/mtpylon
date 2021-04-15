# -*- coding: utf-8 -*-
from typing import Any, Generator
from dataclasses import dataclass, field
import logging

from aiohttp.web import WebSocketResponse

from .types import long
from .messages import message_ids, pack_message, UnencryptedMessage
from .transports import Obfuscator, TransportWrapper
from .schema import Schema

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

    async def send_message(self, data: Any, response: bool = False) -> None:
        if self.ws.closed:
            logger.warning('Ws connection has been closed before')
            return

        message = UnencryptedMessage(
            msg_id=self._msg_ids.send(response),
            value=data
        )

        try:
            message_bytes = await pack_message(message)
        except ValueError as e:
            logger.error(f'Can`t dump message {message} close ws connection')
            logger.error(e)
            await self.ws.close()
        else:
            wrapped_message = self.transport_wrapper.wrap(message_bytes)
            encrypted_data = self.obfuscator.encrypt(wrapped_message)
            msg_type = 'response' if response else 'notification'
            logger.info(f'Send {msg_type} with id {message.msg_id}')
            await self.ws.send_bytes(encrypted_data)
