# -*- coding: utf-8 -*-
from ..constructors import MessageContainer
from mtpylon.serialization import LoadedValue


def dump(msg_container: MessageContainer) -> bytes:
    ...


def load(value: bytes) -> LoadedValue[MessageContainer]:
    ...
