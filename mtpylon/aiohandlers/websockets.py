# -*- coding: utf-8 -*-
import logging
from functools import partial
from typing import cast, Optional, Callable, Awaitable

from aiohttp import WSMsgType
from aiohttp.web import Request, WebSocketResponse

from mtpylon.schema import Schema
from mtpylon.transports import (
    parse_header,
    get_wrapper,
    TransportWrapper,
    Obfuscator
)

logger = logging.getLogger(__name__)

WebSocketHandler = Callable[[Request], Awaitable[WebSocketResponse]]


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
    obfuscator: Optional[Obfuscator] = None
    transport_wrapper: Optional[TransportWrapper] = None

    logger.info("New websocket connection")

    async for msg in ws:
        if msg.type != WSMsgType.BINARY:
            logger.error('MTProto accepts only binary data')
            break
        logger.debug('Handle income message')

        if transport_tag is None:
            try:
                transport_tag, obfuscator = parse_header(msg.data)
                transport_wrapper = get_wrapper(transport_tag)
            except ValueError as e:
                logger.error(str(e))
                break
            else:
                logger.debug(
                    f'Obfuscation,wrapper for {hex(transport_tag)} set'
                )
                continue

        obfuscator = cast(Obfuscator, obfuscator)
        transport_wrapper = cast(TransportWrapper, transport_wrapper)

        try:
            transport_message = obfuscator.decrypt(msg.data)
            message = transport_wrapper.unwrap(transport_message)
            logger.debug('Parse message:', message)
        except ValueError as e:
            logger.error(str(e))
            break

    logger.info("Close websocket connection")
    return ws


def create_websocket_handler(
        schema: Schema
) -> WebSocketHandler:

    return partial(ws_handler, schema=schema)
