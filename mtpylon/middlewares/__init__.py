# -*- coding: utf-8 -*-
from .types import MiddleWareFunc, Handler
from .set_server_salt import set_server_salt
from .set_session_id import set_session_id
from .apply import apply_middleware

BASIC_MIDDLEWARES = [
    set_session_id,
    set_server_salt,
]

__all__ = [
    'MiddleWareFunc',
    'Handler',
    'BASIC_MIDDLEWARES',
    'apply_middleware',
]
