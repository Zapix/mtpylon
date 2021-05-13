# -*- coding: utf-8 -*-
from dataclasses import dataclass

from .types import long


class InvalidCombinator(Exception):
    """
    Raised when wrong combinator has been passed
    """
    pass


class InvalidConstructor(Exception):
    """
    Raised when wrong constructor has been passed
    """
    pass


class InvalidFunction(Exception):
    """
    Raises when wrong mtpytlon function has been passed
    """
    pass


class SchemaChangeError(Exception):
    """
    Raises when user tries add or delete combinator, function after schema
    initialization
    """


class DumpError(Exception):
    """
    Raises error when can't dump object or function call  by schema
    """
    pass


@dataclass
class InvalidMessageError(Exception):
    """
    Raises when invalid message has been received
    """
    error_code: int


@dataclass
class InvalidServerSalt(Exception):
    """
    Raises when message with wrong server_salt has been received
    """
    error_code: int
    new_server_salt: long


class AuthKeyNotFound(Exception):
    """
    Raises when auth key not found in manager by auth key id
    """


class AuthKeyChangedException(Exception):
    """
    Raises when messages with different auth keys in same connection
    """


@dataclass
class RpcCallError(Exception):
    """
    Raises on user rpc call
    """
    error_code: int
    error_message: str
