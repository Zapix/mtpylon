# -*- coding: utf-8 -*-
from aiohttp.web import Request, Response
from aiohttp.web_response import json_response
from mtpylon.contextvars import rsa_manager


async def pub_keys_view(request: Request) -> Response:
    try:
        manager = rsa_manager.get()
    except LookupError:
        response = Response(
            text='Public keys has not been set',
            status=400
        )
    else:
        response = json_response(
            [key.decode() for key in manager.public_key_list],
            status=200
        )

    return response
