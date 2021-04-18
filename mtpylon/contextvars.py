# -*- coding: utf-8 -*-
"""
Declared contextvars that will be used in mtpylon
"""
from contextvars import ContextVar

from aiohttp.web import Request

from . import int128, int256


"""
Stores server_nonces for authorization key creation process
"""
server_nonce_var: ContextVar[int128] = ContextVar('server_nonce')

new_nonce_var: ContextVar[int256] = ContextVar('new_nonce')


"""
Stores p,q, p * q values for init dh exchange process
"""
pq_var: ContextVar[int] = ContextVar('pq')
p_var: ContextVar[int] = ContextVar('p')
q_var: ContextVar[int] = ContextVar('q')

"""
Stores server side DH exchange value
"""
g_var: ContextVar[int] = ContextVar('g')
a_var: ContextVar[int] = ContextVar('a')
dh_prime_var: ContextVar[int] = ContextVar('dh_prime')


"""
Stores request from websocket handler.

NOTE: not sure will request in context has got access to shared request
resources.
"""
ws_request: ContextVar[Request] = ContextVar('ws_request')
