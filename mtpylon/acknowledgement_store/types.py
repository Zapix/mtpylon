# -*- coding: utf-8 -*-
from typing import Any
from dataclasses import dataclass

from mtpylon.crypto import AuthKey
from mtpylon.types import long


@dataclass(frozen=True)
class AcknowledgementMessage:
    message_id: long
    data: Any


@dataclass(frozen=True)
class AuthSessionHash:
    auth_key: AuthKey
    session_id: long
