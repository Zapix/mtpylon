# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any

from mtpylon import long


@dataclass
class Message:
    salt: long
    session_id: long
    message_id: long
    seq_no: int
    message_data: Any


@dataclass
class UnencryptedMessage:
    message_id: long
    message_data: Any
