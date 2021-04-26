# -*- coding: utf-8 -*-
from typing import Protocol, List, Optional

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from .salt import Salt


class ServerSaltManagerProtocol(Protocol):

    async def has_salt(self, auth_key: AuthKey, salt_value: long) -> bool:
        """
        Checks can be current salt been used now or not.
        """
        ...

    async def set_salt(
            self,
            auth_key: AuthKey,
            salt: Salt
    ):
        """
        Sets server salt for auth key
        """
        ...

    async def get_future_salts(
        self,
        auth_key: AuthKey,
        count: int = 1
    ) -> List[Salt]:
        """
        Get or generate future salts for current authorization key .
        Maximum future salts that could be return is 64

        Raises:
            ValueError - if negative or more then 64 values should be returned
        """
        ...

    async def clear(self, auth_key: Optional[AuthKey] = None):
        """
        Clear all outdated server salts
        :param auth_key:
        :return:
        """
        ...
