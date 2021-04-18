# -*- coding: utf-8 -*-
from aiohttp import web

from ..constructors import DestroyAuthKeyOk, DestroyAuthKeyRes


async def destroy_auth_key(request: web.Request) -> DestroyAuthKeyRes:
    return DestroyAuthKeyOk()
