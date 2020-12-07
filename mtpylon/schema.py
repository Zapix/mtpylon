# -*- coding: utf-8 -*-
from typing import List, Callable, Any, NoReturn
from .utils import is_valid_constructor, is_valid_function


class Schema:
    """
    Base schema to load/dump messages by mtproto protocol.
    Validates passed constructors and function that could be used
    in schema. Schema stores constructors and functions and could
    return his representation as dict that could be dumps as json or
    as TL program string(https://core.telegram.org/mtproto/TL#overview)
    """

    def __init__(self, constructors: List[Any], functions: List[Callable]):
        """
        Initial base schema. Validates passed constructors and schemas
        save them for dumping and loading messages
        """
        for constructor in constructors:
            is_valid_constructor(constructor, constructors)

        for func in functions:
            is_valid_function(func, constructors)

        self.constructors = constructors
        self.functions = functions

    def schema_structure(self) -> NoReturn:
        raise NotImplementedError

    def dump(self) -> NoReturn:
        raise NotImplementedError

    def load(self) -> NoReturn:
        raise NotImplementedError
