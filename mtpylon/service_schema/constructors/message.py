# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any

from mtpylon import long


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

    @property
    def message_id(self) -> long:
        return self.msg_id

    @property
    def message_data(self) -> Any:
        return self.body
