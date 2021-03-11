# -*- coding: utf-8 -*-
import asyncio
from typing import Protocol, Union, Dict

from .auth_key import AuthKey
from .exceptions import AuthKeyDoesNotExist


class AuthKeyManagerProtocol(Protocol):

    async def set_key(self, value: Union[AuthKey, int]):  # pragma: nocover
        """
        Sets new available authentication key. This method
        takes instance of AuthKey class or auth_key as integer
        It'll be async function coz we could use separated service to store
        authorization keys
        """
        ...

    async def has_key(
            self,
            value: Union[AuthKey, int]
    ) -> bool:  # pragma: nocover
        """
        Checks is this AuthKey store in manager or not. This method
        takes intance of AuthKey class or integer as auth_key_id.
        It'll be async function coz we could use separated service to store
        authorization keys
        """
        ...

    async def get_key(self, value: int) -> AuthKey:  # pragma: nocover
        """
        Gets auth key data by its id.
        It'll be async function coz we could separated service to store
        authorization keys

        Raises: AuthKeyDoesNotExist if key doesn't store in manager
        """
        ...

    async def del_key(self, value: Union[AuthKey, int]):  # pragma: nocover
        """
        Delete auth key from manager by it's id, value or AuthKey instance
        It'll be async function coz we could use separated service to store
        authorization keys

        Raises:  AuthKeyDoesNotExist if key doesn't store in manager
        """
        ...


class AuthKeyManager(AuthKeyManagerProtocol):

    def __init__(self):
        self._manager_lock = asyncio.Lock()
        self._manager_map: Dict[int, AuthKey] = {}

    async def set_key(self, value: Union[AuthKey, int]):
        if isinstance(value, int):
            value = AuthKey(value)

        async with self._manager_lock:
            self._manager_map[value.id] = value

    async def has_key(self, value: Union[AuthKey, int]) -> bool:
        if isinstance(value, AuthKey):
            value = value.id

        async with self._manager_lock:
            result = value in self._manager_map

        return result

    async def get_key(self, value: int) -> AuthKey:
        async with self._manager_lock:
            try:
                result = self._manager_map[value]
            except KeyError:
                raise AuthKeyDoesNotExist(
                    f'Auth key id {value} does not exist'
                )
        return result

    async def del_key(self, value: Union[AuthKey, int]):
        if isinstance(value, AuthKey):
            value = value.id

        async with self._manager_lock:
            try:
                del self._manager_map[value]
            except KeyError:
                raise AuthKeyDoesNotExist
