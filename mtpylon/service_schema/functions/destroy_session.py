# -*- coding: utf-8 -*-
from aiohttp import web

from ... import long
from ..constructors import DestroySessionRes, DestroySessionOk


async def destroy_session(
    request: web.Request,
    session_id: long
) -> DestroySessionRes:
    return DestroySessionOk(session_id=session_id)
