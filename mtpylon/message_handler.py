# -*- coding: utf-8 -*-
import logging
from typing import cast, Any, List
from dataclasses import dataclass, field
from functools import partial

from aiohttp import web

from .exceptions import InvalidMessageError, InvalidServerSalt
from .schema import Schema
from .serialization import CallableFunc
from .transports import Obfuscator, TransportWrapper
from .message_sender import MessageSender
from .messages import MtprotoMessage, unpack_message
from .service_schema.constructors import (
    BadMessageNotification,
    BadServerSalt
)
from .utils import get_function_name
from .middlewares import MiddleWareFunc
from .contextvars import income_message_var

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
        logger.debug(f'Received message: {message.message_id}')
        income_message_var.set(message)

        result: Any = None

        try:
            self.validate_message(message)
        except InvalidMessageError as e:
            msg_id = message.message_id
            e_code = e.error_code
            logger.error(f'Msg {msg_id}: is invalid message. code: {e_code}')
            result = BadMessageNotification(
                bad_msg_id=msg_id,
                bad_msg_seqno=getattr(message, 'seqno', 0),
                error_code=e.error_code
            )
        except InvalidServerSalt as e:
            msg_id = message.message_id
            logger.error(f'Msg {msg_id}: has bad server salt.')
            logger.info(f'Msg {msg_id}: new server salt: {e.new_server_salt}')
            result = BadServerSalt(
                bad_msg_id=msg_id,
                bad_msg_seqno=getattr(message, 'seqno', 0),
                error_code=e.error_code,
                new_server_salt=e.new_server_salt
            )
        else:
            value = cast(CallableFunc, message.message_data)
            func_name = get_function_name(value.func)
            logger.info(
                f'Msg {message.message_id}: call rpc function: {func_name}'
            )

            handler = value.func

            for middleware in self.middlewares[::-1]:
                handler = partial(middleware, handler)

            result = await handler(request, **value.params)

        logger.info(f'Response to message {message.message_id}')
        await self.message_sender.send_message(request, result, response=True)

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

    def validate_message(self, msg: MtprotoMessage) -> MtprotoMessage:
        """
        Validate message and returns it.

        Raises:
            InvalidMessageError - when wrong message has been received

        :param msg:
        :return:
        """
        ...
