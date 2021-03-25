# -*- coding: utf-8 -*-
"""
Declared contextvars that will be used in mtpylon
"""
from contextvars import ContextVar

from .crypto.rsa_manager import RsaManagerProtocol
from .dh_prime_generators.typing import DhPrimeGenerator
from .utils import int128

"""
Store rsa_manager in context to get access for all values.
Probably should be global variable.
"""
rsa_manager: ContextVar[RsaManagerProtocol] = ContextVar('rsa_manager')


"""
Store dh_prime generator that returns 2048-bit safe prime numbers.
Coz 2048-values are to big we assume that it'll be async generator
"""
dh_prime_generator: ContextVar[DhPrimeGenerator] = ContextVar(
    'dh_prime_generator'
)


"""
Stores server_nonces for authorization key creation process
"""
server_nonce: ContextVar[int128] = ContextVar('server_nonce')


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
