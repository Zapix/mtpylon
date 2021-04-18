# -*- coding: utf-8 -*-
from aiohttp import web

from ... import long
from ..constructors import Pong


async def ping_delay_disconnect(
        request: web.Request,
        ping_id: long,
        disconnect_delay: int
) -> Pong:
    return Pong(
        msg_id=long(123),
        ping_id=ping_id,
    )
