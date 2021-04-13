# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long


@dataclass
class FutureSalt:
    valid_since: int
    valid_until: int
    salt: long

    class Meta:
        name = 'future_salt'
        order = ('valid_since', 'valid_until', 'salt')
