# -*- coding: utf-8 -*-
from typing import Callable, Awaitable, Any, cast

from aiohttp.web import Request

from mtpylon.messages import Message
from mtpylon.salts import ServerSaltManagerProtocol, Salt
from mtpylon.service_schema.constructors import BadServerSalt
from mtpylon.contextvars import auth_key_var, income_message_var


async def set_server_salt(
    handler: Callable[..., Awaitable[Any]],
    request: Request,
    **params
) -> Any:
    message = income_message_var.get()

    if isinstance(message, Message):
        auth_key = auth_key_var.get()
        server_salt_manager = request.app.get(
            'server_salt_manager'
        )

        server_salt_manager = cast(
            ServerSaltManagerProtocol,
            server_salt_manager
        )

        if not await server_salt_manager.has_salt(auth_key, message.salt):
            new_salts = await server_salt_manager.get_future_salts(auth_key)
            new_salt: Salt = new_salts[0]

            return BadServerSalt(
                bad_msg_id=message.message_id,
                bad_msg_seqno=message.seq_no,
                error_code=48,
                new_server_salt=new_salt.salt
            )

    return await handler(request, **params)
