# -*- coding: utf-8 -*-
from typing import NewType, Any

long = NewType('long', int)
int128 = NewType('int128', int)
int256 = NewType('int256', int)
double = NewType('double', float)
BASIC_TYPES = [str, bytes, int, long, int128, int256, double, Any]
