# -*- coding: utf-8 -*-
import logging
from functools import partial
from typing import cast, Optional
from asyncio import create_task

from aiohttp import WSMsgType
from aiohttp.web import Request, WebSocketResponse

from mtpylon.aiohandlers.types import WebSocketHandler
from mtpylon.schema import Schema
from mtpylon.transports import (
    parse_header,
    get_wrapper,
)
from mtpylon.message_sender import MessageSender
from mtpylon.message_handler import MessageHandler
from mtpylon.contextvars import ws_request

logger = logging.getLogger(__name__)


async def ws_handler(request: Request, schema: Schema) -> WebSocketResponse:
    """
    Websocket handler that works with MTProto protocol.
    MTProto works only with binary data so close connection if not binary
    data has been sent.
    First of all gets mtproto transport obfuscation header to
    understand how to decrypt obfuscated messages and what transport
    protocol should be used.
    If server didn't receive current data - close connection
    """

    ws = WebSocketResponse()
    await ws.prepare(request)

    transport_tag: Optional[int] = None
    message_handler: Optional[MessageHandler] = None
    message_sender: Optional[MessageSender] = None

    logger.info("New websocket connection")

    async for msg in ws:
        if msg.type != WSMsgType.BINARY:
            logger.error('MTProto accepts only binary data')
            break
        data = cast(bytes, msg.data)
        logger.debug('Handle income message')

        if transport_tag is None:
            try:
                transport_tag, obfuscator = parse_header(data)
                transport_wrapper = get_wrapper(transport_tag)
                message_sender = MessageSender(
                    schema=schema,
                    obfuscator=obfuscator,
                    transport_wrapper=transport_wrapper,
                    ws=ws,
                )
                message_handler = MessageHandler(
                    schema=schema,
                    obfuscator=obfuscator,
                    transport_wrapper=transport_wrapper,
                    message_sender=message_sender
                )
                ws_request.set(request)
            except ValueError as e:
                logger.error(str(e))
                break
            else:
                logger.debug(
                    f'Obfuscation,wrapper for {hex(transport_tag)} set'
                )
                continue

        message_handler = cast(MessageHandler, message_handler)
        try:
            create_task(message_handler.handle(data))
        except ValueError as e:
            logger.error(str(e))
            break

    logger.info("Close websocket connection")
    return ws


def create_websocket_handler(
        schema: Schema
) -> WebSocketHandler:

    return partial(ws_handler, schema=schema)
