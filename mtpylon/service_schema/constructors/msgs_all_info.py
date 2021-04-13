# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from mtpylon import long


@dataclass
class MsgsAllInfo:
    msg_ids: List[long]
    info: bytes

    class Meta:
        name = 'msgs_all_info'
        order = ('msg_ids', 'info')
