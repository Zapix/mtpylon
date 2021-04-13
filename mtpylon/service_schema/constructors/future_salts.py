# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from ... import long
from .future_salt import FutureSalt


@dataclass
class FutureSalts:
    req_msg_id: long
    now: int
    salts: List[FutureSalt]

    class Meta:
        name = 'future_salts'
        order = ('req_msg_id', 'now', 'salts')
