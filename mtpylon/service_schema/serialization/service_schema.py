# -*- coding: utf-8 -*-
from typing import Any

from mtpylon.serialization import (
    load as load_schema,
    dump as dump_schema,
    LoadedValue,
)

from ..service_schema import service_schema
from ..constructors import Message
from .message import dump as dump_message, load as load_message


def dump(value: Any, **kwargs: Any) -> bytes:
    """
    Dumps service schema values, rpc calls. Uses custom dumper for
    Message type
    """
    return dump_schema(
        service_schema,
        value,
        custom_dumpers={
            Message: dump_message,
        },
        **kwargs
    )


def load(input: bytes) -> LoadedValue[Any]:
    """
    Loads service schema value, rpc call from data. uses custom loader for
    Message type
    """
    return load_schema(
        service_schema,
        input,
        custom_loaders={
            Message: load_message,
        }
    )
