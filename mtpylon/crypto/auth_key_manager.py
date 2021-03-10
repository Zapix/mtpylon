# -*- coding: utf-8 -*-
from typing import Protocol, Union

from .auth_key import AuthKey


class AuthKeyManagerProtocol(Protocol):

    async def set_key(self, value: Union[AuthKey, int]):
        """
        Sets new available authentication key. This method
        takes instance of AuthKey class or auth_key as integer
        It'll be async function coz we could use separated service to store
        authorization keys
        """
        ...

    async def hash_key(self, value: Union[AuthKey, int]) -> bool:
        """
        Checks is this AuthKey store in manager or not. This method
        takes intance of AuthKey class or integer as auth_key_id.
        It'll be async function coz we could use separated service to store
        authorization keys
        """
        ...

    async def get_key(self, value: int) -> AuthKey:
        """
        Gets auth key data by its id.
        It'll be async function coz we could separated service to store
        authorization keys
        """
        ...
