# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long


@dataclass
class Pong:
    msg_id: long
    ping_id: long

    class Meta:
        name = 'pong'
        order = ('msg_id', 'ping_id')
