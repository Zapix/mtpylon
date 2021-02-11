# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any

from mtpylon.utils import long


@dataclass
class Message:
    msg_id: long
    seqno: int
    bytes: int
    body: Any

    class Meta:
        name = 'message'
        order = (
            'msg_id',
            'seqno',
            'bytes',
            'body',
        )
