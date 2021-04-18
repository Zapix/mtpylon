# -*- coding: utf-8 -*-
from aiohttp import web

from mtpylon.types import long
from ..constructors import RpcDropAnswer, RpcAnswerUnknown


async def rpc_drop_answer(
    request: web.Request,
    req_msg_id: long
) -> RpcDropAnswer:
    return RpcAnswerUnknown()
