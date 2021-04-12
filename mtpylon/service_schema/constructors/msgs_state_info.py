# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long


@dataclass
class MsgsStateInfo:
    req_msg_id: long
    info: bytes

    class Meta:
        name = 'msgs_state_info'
        order = ('req_msg_id', 'info')
