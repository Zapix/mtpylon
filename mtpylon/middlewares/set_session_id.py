# -*- coding: utf-8 -*-
import logging
from typing import Any

from aiohttp.web import Request

from mtpylon.constants import SESSION_SUBJECT_RESOURCE_NAME
from mtpylon.contextvars import income_message_var, session_id_var
from mtpylon.messages import EncryptedMessage

from .types import Handler

logger = logging.getLogger(__name__)


async def set_session_id(
    handler: Handler,
    request: Request,
    **params: Any,
) -> Any:
    session_subject = request.app[SESSION_SUBJECT_RESOURCE_NAME]
    income_message = income_message_var.get()

    if isinstance(income_message, EncryptedMessage):
        if not await session_subject.has_session(income_message.session_id):
            await session_subject.create_session(income_message.session_id)

        logger.info(f'Set session id: {income_message.session_id}')

        session_id_var.set(income_message.session_id)

    return await handler(request, **params)
