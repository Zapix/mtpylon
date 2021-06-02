# -*- coding: utf-8 -*-
from typing import cast, List
from asyncio import create_task

from aiohttp.web import Request

from mtpylon.income_message import IncomeMessage
from mtpylon.message_sender import MessageSender
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.messages import EncryptedMessage
from mtpylon.service_schema.constructors import MsgsAck
from mtpylon.contextvars import auth_key_var


async def handle_msgs_ack(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage
):
    message = cast(EncryptedMessage, message)
    msgs_ack = cast(MsgsAck, message.message_data)

    auth_key = auth_key_var.get()
    session_id = message.session_id

    acknowledgement_store = request.app['acknowledgement_store']

    for msg_id in msgs_ack.msg_ids:
        create_task(
            acknowledgement_store.delete_message(
                auth_key,
                session_id,
                msg_id
            )
        )
