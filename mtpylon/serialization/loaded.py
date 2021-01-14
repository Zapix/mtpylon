# -*- coding: utf-8 -*-
from typing import TypeVar, Generic, Final

Value = TypeVar('Value')


class LoadedValue(Generic[Value]):

    def __init__(self, value: Value, offset: int) -> None:
        self.value: Final[Value] = value
        self.offset: Final[int] = offset
