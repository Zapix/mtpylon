# -*- coding: utf-8 -*-
from ...utils import long
from ..constructors import RpcDropAnswer, RpcAnswerUnknown


async def rpc_drop_answer(req_msg_id: long) -> RpcDropAnswer:
    return RpcAnswerUnknown()
