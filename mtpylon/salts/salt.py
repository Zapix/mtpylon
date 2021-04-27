# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import getrandbits

from mtpylon import long


def random_long() -> long:
    return long(getrandbits(64))


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
