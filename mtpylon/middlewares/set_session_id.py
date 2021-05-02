# -*- coding: utf-8 -*-
from typing import Callable, Awaitable, Any

from aiohttp.web import Request

from mtpylon.contextvars import income_message_var
from mtpylon.messages import Message


async def set_session_id(
    handler: Callable[..., Awaitable[Any]],
    request: Request,
    **params
):
    session_subject = request.app['session_subject']
    income_message = income_message_var.get()

    if isinstance(income_message, Message):
        if not await session_subject.has_session(income_message.session_id):
            await session_subject.create_session(income_message.session_id)

    return await handler(request, **params)
