# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from mtpylon import long


@dataclass
class MsgsAck:
    msg_ids: List[long]

    class Meta:
        name = 'msgs_ack'
        order = ('msg_ids',)
