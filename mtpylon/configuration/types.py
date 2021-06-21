# -*- coding: utf-8 -*-
from typing import TypedDict, NewType, Dict, Any

ClassPath = NewType('ClassPath', str)


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
    manager: ClassPath
    params: Dict[str, Any]


class ConfigDict(TypedDict):
    """
    Config for whole mtpylon application that should be passed to configure
    asyncio.web.Application instance.
    Config Dict has got several parts:
     * `rsa_manager` - configure available rsa_keys. check it with
     `RsaManagerDict` info.
    """
    rsa_manager: RsaManagerDict
