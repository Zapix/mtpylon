# -*- coding: utf-8 -*-
from aiohttp.web import Request, Response
from aiohttp.web_response import json_response

from mtpylon.constants import RSA_MANAGER_RESOURCE_NAME


async def pub_keys_view(request: Request) -> Response:
    if RSA_MANAGER_RESOURCE_NAME not in request.app:
        response = Response(
            text='Public keys has not been set',
            status=400
        )
    else:
        rsa_manager = request.app[RSA_MANAGER_RESOURCE_NAME]

        response = json_response(
            [key.decode() for key in rsa_manager.public_key_list],
            status=200
        )

    return response
