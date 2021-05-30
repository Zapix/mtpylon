# -*- coding: utf-8 -*-
from typing import Any
from dataclasses import dataclass

from mtpylon.types import long


@dataclass(frozen=True)
class AcknowledgementMessage:
    message_id: long
    data: Any
