# -*- coding: utf-8 -*-
from aiohttp import web

from ... import long
from ..constructors import FutureSalts


async def get_future_salts(
    request: web.Request,
    num: int
) -> FutureSalts:
    return FutureSalts(
        req_msg_id=long(1),
        now=num,
        salts=[]
    )
