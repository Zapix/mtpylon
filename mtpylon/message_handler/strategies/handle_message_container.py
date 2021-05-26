# -*- coding: utf-8 -*-
from typing import cast, Callable, List, Any
from asyncio import create_task

from aiohttp.web import Request

from mtpylon.income_message import IncomeMessage
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.message_sender import MessageSender
from mtpylon.contextvars import income_message_var
from mtpylon.service_schema.constructors import MessageContainer
from mtpylon.middlewares import apply_middleware

from .types import HandleStrategy


async def _message_container_handler(
    request: Request,
    **kwargs: Any
):
    """
    Blank handler to apply middlewares for message container
    """
    ...


async def handle_message_container(
    strategy_selector: Callable[[IncomeMessage], HandleStrategy],
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage
):
    income_message_var.set(message)

    handler = apply_middleware(middlewares, _message_container_handler)

    await handler(request)

    message_container = cast(
        MessageContainer,
        message.message_data
    )

    for inner_message in message_container.messages:
        message_handler = strategy_selector(inner_message)
        create_task(
            message_handler(
                middlewares,
                sender,
                request,
                inner_message
            )
        )
