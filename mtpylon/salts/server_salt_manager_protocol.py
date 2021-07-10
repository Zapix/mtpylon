# -*- coding: utf-8 -*-
from typing import Protocol, List, Optional

from mtpylon.types import long
from mtpylon.crypto import AuthKey
from .salt import Salt


class ServerSaltManagerProtocol(Protocol):

    async def has_salt(
        self,
        auth_key: AuthKey,
        salt_value: long
    ) -> bool:  # pragma: nocover
        """
        Checks can current salt be used now or not.
        """
        ...

    async def set_salt(
            self,
            auth_key: AuthKey,
            salt: Salt
    ):  # pragma: nocover
        """
        Sets server salt for auth key
        """
        ...

    async def get_future_salts(
        self,
        auth_key: AuthKey,
        count: int = 1
    ) -> List[Salt]:  # pragma: nocover
        """
        Get or generate future salts for current authorization key .
        Maximum future salts that could be return is 64

        Raises:
            ValueError - if negative or more then 64 values should be returned
        """
        ...

    async def clear(
        self,
        auth_key: Optional[AuthKey] = None
    ):  # pragma: nocover
        """
        Clear all outdated server salts
        :param auth_key:
        :return:
        """
        ...
