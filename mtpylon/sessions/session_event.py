# -*- coding: utf-8 -*-
from typing import Literal
from dataclasses import dataclass

from mtpylon.types import long
from mtpylon.crypto import AuthKey


EventType = Literal['created', 'destroyed']


@dataclass(frozen=True)
class SessionEvent:
    type: EventType
    session_id: long
    auth_key: AuthKey
