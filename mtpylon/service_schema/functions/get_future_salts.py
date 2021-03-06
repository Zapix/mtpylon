# -*- coding: utf-8 -*-
from ...utils import long
from ..constructors import FutureSalts


async def get_future_salts(num: int) -> FutureSalts:
    return FutureSalts(
        req_msg_id=long(1),
        now=num,
        salts=[]
    )
