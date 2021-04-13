# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import long


@dataclass
class DestroySessionOk:
    session_id: long

    class Meta:
        name = 'destroy_session_ok'
        order = ('session_id',)


@dataclass
class DestroySessionNone:
    session_id: long

    class Meta:
        name = 'destroy_session_none'
        order = ('session_id',)


DestroySessionRes = Annotated[
    Union[
        DestroySessionOk,
        DestroySessionNone
    ],
    'DestroySessionRes'
]
