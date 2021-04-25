# -*- coding: utf-8 -*-
"""
Declared contextvars that will be used in mtpylon
"""
from typing import Optional
from contextvars import ContextVar

from .types import int128, int256, long
from .crypto import AuthKey


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


"Stores auth key for current context"
auth_key_var: ContextVar[AuthKey] = ContextVar('auth_key')


"""
Stores server salt
"""
server_salt_var: ContextVar[Optional[long]] = ContextVar('server_salt')


"""
Stores session id
"""
session_id_var: ContextVar[Optional[long]] = ContextVar('session_id')
