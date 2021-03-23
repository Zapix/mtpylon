# -*- coding: utf-8 -*-
"""
Declared contextvars that will be used in mtpylon
"""
from contextvars import ContextVar

from .crypto.rsa_manager import RsaManagerProtocol
from .utils import int128, long


"""
Store rsa_manager in context to get access for all values.
Probably should be global variable.
"""
rsa_manager: ContextVar[RsaManagerProtocol] = ContextVar('rsa_manager')


server_nonce: ContextVar[int128] = ContextVar('server_nonce')


pq: ContextVar[bytes] = ContextVar('pq')
p: ContextVar[long] = ContextVar('p')
q: ContextVar[long] = ContextVar('q')
