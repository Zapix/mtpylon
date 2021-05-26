# -*- coding: utf-8 -*-
import logging
from typing import cast, List

from aiohttp.web import Request

from mtpylon.messages import UnencryptedMessage
from mtpylon.serialization import CallableFunc
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.message_sender import MessageSender
from mtpylon.contextvars import income_message_var
from mtpylon.utils import get_function_name
from mtpylon.middlewares import apply_middleware
from mtpylon.income_message import IncomeMessage

logger = logging.getLogger(__name__)


async def handle_unencrypted_message(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage,
):
    """
    Handles unencrypted message. Applies all middlewares to sender function
    and sends message
    """
    message = cast(UnencryptedMessage, message)

    income_message_var.set(message)

    value = cast(CallableFunc, message.message_data)
    func_name = get_function_name(value.func)

    logger.info(
        f'Msg {message.message_id}: call rpc function: {func_name}'
    )

    handler = apply_middleware(middlewares, value.func)

    result = await handler(request, **value.params)

    logger.info(f'Response to message {message.message_id}')

    await sender.send_unencrypted_message(request, result, response=True)
