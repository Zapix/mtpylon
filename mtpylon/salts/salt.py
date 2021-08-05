# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import getrandbits

from mtpylon.types import long


def random_long() -> long:
    val_bytes = getrandbits(64).to_bytes(8, 'little')
    return long(int.from_bytes(val_bytes, 'little', signed=True))


def now() -> datetime:
    return datetime.now()


def tomorrow() -> datetime:
    return datetime.now() + timedelta(days=1)


@dataclass(frozen=True)
class Salt:
    """
    Stores valid salt
    """
    salt: long = field(default_factory=random_long, hash=True)
    since: datetime = field(default_factory=now, hash=False)
    until: datetime = field(default_factory=tomorrow, hash=False)
