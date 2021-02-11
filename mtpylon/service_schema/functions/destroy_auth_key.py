# -*- coding: utf-8 -*-
from ..constructors import DestroyAuthKeyOk, DestroyAuthKeyRes


async def destroy_auth_key() -> DestroyAuthKeyRes:
    return DestroyAuthKeyOk()
