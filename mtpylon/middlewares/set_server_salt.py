# -*- coding: utf-8 -*-
import logging
from typing import Any, cast

from aiohttp.web import Request

from mtpylon.constants import SERVER_SALT_MANAGER_RESOURCE_NAME
from mtpylon.messages import EncryptedMessage
from mtpylon.salts import ServerSaltManagerProtocol, Salt
from mtpylon.service_schema.constructors import BadServerSalt
from mtpylon.contextvars import (
    auth_key_var,
    income_message_var,
    server_salt_var,
)
from .types import Handler

logger = logging.getLogger(__name__)


async def set_server_salt(
    handler: Handler,
    request: Request,
    **params: Any,
) -> Any:
    message = income_message_var.get()

    if isinstance(message, EncryptedMessage):
        logger.info(f'Check server salt {message.salt}')
        auth_key = auth_key_var.get()
        server_salt_manager = request.app.get(
            SERVER_SALT_MANAGER_RESOURCE_NAME
        )

        logger.info(f'Set salt {message.salt}')
        server_salt_var.set(message.salt)

        server_salt_manager = cast(
            ServerSaltManagerProtocol,
            server_salt_manager
        )

        if not await server_salt_manager.has_salt(auth_key, message.salt):
            logger.info('Bad serversalt has been used')
            new_salts = await server_salt_manager.get_future_salts(auth_key)
            new_salt: Salt = new_salts[0]

            return BadServerSalt(
                bad_msg_id=message.message_id,
                bad_msg_seqno=message.seq_no,
                error_code=48,
                new_server_salt=new_salt.salt
            )

    return await handler(request, **params)
