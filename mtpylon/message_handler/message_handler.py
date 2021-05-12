# -*- coding: utf-8 -*-
import logging
from typing import List
from dataclasses import dataclass, field

from aiohttp import web

from mtpylon.schema import Schema
from mtpylon.transports import Obfuscator, TransportWrapper
from mtpylon.message_sender import MessageSender
from mtpylon.messages import MtprotoMessage, unpack_message
from mtpylon.middlewares import MiddleWareFunc

from .strategies import get_handle_strategy

logger = logging.getLogger(__name__)


@dataclass
class MessageHandler:
    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    message_sender: MessageSender
    middlewares: List[MiddleWareFunc] = field(default_factory=list)

    async def handle(self, request: web.Request, obfuscated_data: bytes):
        message = await self.decrypt_message(request, obfuscated_data)
        logger.info(f'Received message: {message.message_id}')
        logger.debug(message)

        handler = get_handle_strategy(message)

        await handler(self.middlewares, self.message_sender, request, message)

    async def decrypt_message(
            self,
            request: web.Request,
            obfuscated_data: bytes
    ) -> MtprotoMessage:
        transport_message = self.obfuscator.decrypt(obfuscated_data)
        message_bytes = self.transport_wrapper.unwrap(transport_message)

        return await unpack_message(
            request.app['auth_key_manager'],
            self.schema,
            message_bytes
        )
