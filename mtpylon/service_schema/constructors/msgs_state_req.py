# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from mtpylon import long


@dataclass
class MsgsStateReq:
    msg_ids: List[long]

    class Meta:
        name = 'msgs_state_req'
        order = ('msg_ids', )
