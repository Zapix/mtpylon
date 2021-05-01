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
from .messages import UnencryptedMessage, unpack_message
from .service_schema.constructors import (
    BadMessageNotification,
    BadServerSalt
)
from .utils import get_function_name
from .middlewares import MiddleWareFunc
from .contextvars import message_id_var

logger = logging.getLogger(__name__)


@dataclass
class MessageHandler:
    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    message_sender: MessageSender
    middlewares: List[MiddleWareFunc] = field(default_factory=list)

    async def handle(self, request: web.Request, obfuscated_data: bytes):
        message = await self.decrypt_message(obfuscated_data)
        logger.debug(f'Received message: {message.msg_id}')
        self.set_message_context_vars(message)

        result: Any = None

        try:
            self.validate_message(message)
        except InvalidMessageError as e:
            msg_id = message.msg_id
            e_code = e.error_code
            logger.error(f'Msg {msg_id}: is invalid message. code: {e_code}')
            result = BadMessageNotification(
                bad_msg_id=msg_id,
                bad_msg_seqno=getattr(message, 'seqno', 0),
                error_code=e.error_code
            )
        except InvalidServerSalt as e:
            msg_id = message.msg_id
            logger.error(f'Msg {msg_id}: has bad server salt.')
            logger.info(f'Msg {msg_id}: new server salt: {e.new_server_salt}')
            result = BadServerSalt(
                bad_msg_id=msg_id,
                bad_msg_seqno=getattr(message, 'seqno', 0),
                error_code=e.error_code,
                new_server_salt=e.new_server_salt
            )
        else:
            value = cast(CallableFunc, message.value)
            func_name = get_function_name(value.func)
            logger.info(
                f'Msg {message.msg_id}: call rpc function: {func_name}'
            )

            handler = value.func

            for middleware in self.middlewares[::-1]:
                handler = partial(middleware, handler)

            result = await handler(request, **value.params)

        logger.info(f'Response to message {message.msg_id}')
        await self.message_sender.send_message(result, response=True)

    async def decrypt_message(
            self,
            obfuscated_data: bytes
    ) -> UnencryptedMessage:
        transport_message = self.obfuscator.decrypt(obfuscated_data)
        message_bytes = self.transport_wrapper.unwrap(transport_message)

        return await unpack_message(message_bytes)

    def validate_message(self, msg: UnencryptedMessage) -> UnencryptedMessage:
        """
        Validate message and returns it.

        Raises:
            InvalidMessageError - when wrong message has been received

        :param msg:
        :return:
        """
        ...

    def set_message_context_vars(self, message: UnencryptedMessage):
        """
        Sets message_id, server_salt, session_id into context vars
        """
        message_id_var.set(message.msg_id)
