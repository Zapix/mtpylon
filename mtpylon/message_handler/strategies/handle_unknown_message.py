# -*- coding: utf-8 -*-
import logging
from typing import List

from aiohttp.web import Request

from mtpylon.messages import MtprotoMessage
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.message_sender import MessageSender

logger = logging.getLogger(__name__)


async def handle_unknown_message(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: MtprotoMessage,
):
    """
    Logs that we don't know how to handle this message
    """
    logger.warning(f'Unknown message: {message}')
