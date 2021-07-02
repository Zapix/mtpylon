# -*- coding: utf-8 -*-
from typing import TypedDict, Dict, Any

ImportPath = str


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


class AcknowledgmentStoreDict(TypedDict, total=False):
    """
    Stores inofrmation about how to configure acknowledgement storage.
    By default `mtpylon.acknowledgement_store.inmemmory_acknowledgement.`
    `InmemmoryAcknolwedgementStore`. Customer could create it's own
    acknowledgement store by implementing
    `mtpylon.acknowledgement_store.acknowledgement_store_protocol`
    `AcknowlegementStoreProtocol` and pass path to implementation calss
    in `storage` key. Params for this class should be declared in `params`
    dict
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
     * `auth_key_manager` - configure auth key manager. Check
     `AuthKeyManagerDict`
     * `dh_prime_generator` - configure dh prime generator. Check
     `DhPrimeGeneratorDict`
     * `server_salt_manager` - configure server salt manager shared resource.
     Check `ServerSaltManagerDict`
     * `session_storage` - configure resource for storing session info.
     Check `SessionStorageDict`
     * `acknowledgement_storage` - configure resource for storing
     messages that required acknowledgement. Check `AcknowledgementStoreDict`
     * `pub_keys_path` - uri for displaying pub keys view
     * `schema_path`` - uri for displaying schema
     * `api_path` - uri for displaying api by default `/ws`
    """
    rsa_manager: RsaManagerDict
    auth_key_manager: AuthKeyManagerDict
    dh_prime_generator: DhPrimeGeneratorDict
    server_salt_manager: ServerSaltManagerDict
    session_storage: SessionStorageDict
    acknowledgement_storage: AcknowledgmentStoreDict
    pub_keys_path: str
    schema_path: str
    api_path: str
