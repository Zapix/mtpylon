# -*- coding: utf-8 -*-
from typing import cast, List
from asyncio import create_task

from aiohttp.web import Request

from mtpylon.types import long
from mtpylon.constants import ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
from mtpylon.income_message import IncomeMessage
from mtpylon.message_sender import MessageSender
from mtpylon.middlewares import Handler, MiddleWareFunc, apply_middleware
from mtpylon.messages import EncryptedMessage
from mtpylon.service_schema.constructors import MsgsAck
from mtpylon.contextvars import (
    auth_key_var,
    session_id_var,
    income_message_var
)


async def delete_msgs(request: Request, msg_ids: List[long]):
    acknowledgement_store = request.app[ACKNOWLEDGEMENT_STORE_RESOURCE_NAME]

    auth_key = auth_key_var.get()
    session_id = session_id_var.get()

    for msg_id in msg_ids:
        create_task(
            acknowledgement_store.delete_message(
                auth_key,
                session_id,
                msg_id
            )
        )


async def handle_msgs_ack(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage
):
    message = cast(EncryptedMessage, message)
    msgs_ack = cast(MsgsAck, message.message_data)

    income_message_var.set(message)

    handler = cast(Handler, delete_msgs)
    handler = apply_middleware(middlewares, handler)

    await handler(request, msg_ids=msgs_ack.msg_ids)
