# -*- coding: utf-8 -*-
from typing import List
from functools import partial

from .types import MiddleWareFunc, Handler


def apply_middleware(
    middlewares: List[MiddleWareFunc],
    handler: Handler
) -> Handler:
    for middleware in middlewares[::-1]:
        handler = partial(middleware, handler)

    return handler
