# -*- coding: utf-8 -*-
import logging
from typing import cast, Any
from dataclasses import dataclass

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


logger = logging.getLogger(__name__)


@dataclass
class MessageHandler:
    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    message_sender: MessageSender

    async def handle(self, request: web.Request, obfuscated_data: bytes):
        message = await self.decrypt_message(obfuscated_data)
        logger.debug(f'Received message: {message.msg_id}')

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
            result = await value.func(request, **value.params)

        logger.info(f'Response to message {message.msg_id}')
        await self.message_sender.send_message(result, response=True)

    async def decrypt_message(
            self,
            obfuscated_data: bytes
    ) -> UnencryptedMessage:
        transport_message = self.obfuscator.decrypt(obfuscated_data)
        message_bytes = self.transport_wrapper.unwrap(transport_message)

        logger.debug(message_bytes)
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
