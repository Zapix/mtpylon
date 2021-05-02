# -*- coding: utf-8 -*-
from .types import MiddleWareFunc
from .set_server_salt import set_server_salt
from .set_session_id import set_session_id

BASIC_MIDDLEWARES = [
    set_session_id,
    set_server_salt,
]

__all__ = [
    'MiddleWareFunc',
    'BASIC_MIDDLEWARES'
]
