# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class KeyIvPair:
    key: bytes
    iv: bytes
