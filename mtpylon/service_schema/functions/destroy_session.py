# -*- coding: utf-8 -*-
from ... import long
from ..constructors import DestroySessionRes, DestroySessionOk


async def destroy_session(session_id: long) -> DestroySessionRes:
    return DestroySessionOk(session_id=session_id)
