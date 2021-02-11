# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union


@dataclass
class DestroyAuthKeyOk:
    class Meta:
        name = 'destroy_auth_key_ok'


@dataclass
class DestroyAuthKeyNone:
    class Meta:
        name = 'destroy_auth_key_none'


@dataclass
class DestroyAuthKeyFail:
    class Meta:
        name = 'destroy_auth_key_fail'


DestroyAuthKeyRes = Annotated[
    Union[
        DestroyAuthKeyOk,
        DestroyAuthKeyNone,
        DestroyAuthKeyFail,
    ],
    'DestroyAuthKeyRes'
]
