# -*- coding: utf-8 -*-
from typing import Callable, NamedTuple

WrapFunc = Callable[[bytes], bytes]
UnwrapFunc = Callable[[bytes], bytes]


class TransportWrapper(NamedTuple):
    protocol_tag: int
    wrap: WrapFunc
    unwrap: UnwrapFunc
