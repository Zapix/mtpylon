# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any, Union

from mtpylon import long


@dataclass
class EncryptedMessage:
    salt: long
    session_id: long
    message_id: long
    seq_no: int
    message_data: Any


@dataclass
class UnencryptedMessage:
    message_id: long
    message_data: Any


MtprotoMessage = Union[UnencryptedMessage, EncryptedMessage]
