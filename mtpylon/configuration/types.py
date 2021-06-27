# -*- coding: utf-8 -*-
from typing import TypedDict, NewType, Dict, Any

ImportPath = NewType('ImportPath', str)


class RsaManagerDict(TypedDict, total=False):
    """
    Stores information about how to configure rsa_manager for mtpylon
    application. By default we use instance of
    `mtpylon.crypto.rsa_manager.RsaManager` class, that stores info about
    available rsa key pairs. To pass available key pairs uses 'rsa_keys'
    param which should be list of `mtpylon.crypto.rsa_manage.KeyPairs`
    Customer could create it's own rsa_manager that should implement
    `mtpylon.crypto.rsa_manager.RsaManagerProtocol`
    """
    manager: ImportPath
    params: Dict[str, Any]


class AuthKeyManagerDict(TypedDict, total=False):
    """
    Stores information about how to configure auth_key_manager for mtpylon
    application. By default we use instance of
    `mtpylon.crypto.auth_key_manager.AuthKeyManager` class, that stores info
    about registered auth_keys. Customer could create it's own auth_key_manager
    that should implement
    `mtpylon.crypto.auth_key_manager.AuthKeyManagerProtocol`. To pass
    params for creating instance of auth key manager  use `params` value
    that should be a dict with key as string and value as any available type
    """
    manager: ImportPath
    params: Dict[str, Any]


class DhPrimeGeneratorDict(TypedDict, total=False):
    """
    Stores information about default dh prime number generator that will
    generate 2048-bit prime numbers. By default we will get prime numbers
    from 2ton.com.au using `mtpylon.dh_prime_generators.two_tone.generator`
    Customer could creates it's one generator. Generator should be async
    and return `int` values. Additional params could be passed with `param`
    attribute
    """
    generator: ImportPath
    params: Dict[str, Any]


class ServerSaltManagerDict(TypedDict, total=False):
    """
    Stores information about server salt manager. By default
    `mtpylon.salts.server_salt_manager.ServerSaltManager` will be used.
    Customer could create it's own server salt manager with implementing
    `mtpylon.salts.server_salt_manager_protocol.ServerSaltManagerProtocol`
    and passing path to it in 'manager' key. You could pass params to
    initialize instance as dict in 'params' attribute
    """
    manager: ImportPath
    params: Dict[str, Any]


class SessionStorageDict(TypedDict, total=False):
    """
    Stores information about how to configure session storage instance.
    By default
    `mtpylon.sessions.in_memory_session_storage.InMemorySessionStorage` would
    be used. User could create it's own session storage by implementing
    `mtpylon.sessions.SessionStorageProtocol` and pass to it as path in
    `storage` param.
    """
    storage: ImportPath
    params: Dict[str, Any]


class ConfigDict(TypedDict, total=False):
    """
    Config for whole mtpylon application that should be passed to configure
    asyncio.web.Application instance.
    Config Dict has got several parts:
     * `rsa_manager` - configure available rsa_keys. check it with
     `RsaManagerDict` info.
    """
    rsa_manager: RsaManagerDict
    auth_key_manager: AuthKeyManagerDict
    dh_prime_generator: DhPrimeGeneratorDict
    server_salt_manager: ServerSaltManagerDict
    session_storage: SessionStorageDict