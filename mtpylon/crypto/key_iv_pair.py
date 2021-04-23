# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass(frozen=True)
class KeyIvPair:
    key: bytes
    iv: bytes
