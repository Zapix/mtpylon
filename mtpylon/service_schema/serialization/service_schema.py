# -*- coding: utf-8 -*-
from typing import Any, Optional

from mtpylon.serialization import (
    load as load_schema,
    dump as dump_schema,
    LoadedValue,
)
from mtpylon.schema import Schema

from ..service_schema import service_schema
from ..constructors import Message
from .message import dump as dump_message, load as load_message


def dump(value: Any, schema: Optional[Schema] = None) -> bytes:
    """
    Dumps service schema values, rpc calls. Uses custom dumper for
    Message type

    Args:
        value: - object that should be dumped
        schema: common schema(where joined customer and service schema). If
                schema not passed use only service_schema
    """
    if schema is None:
        schema = service_schema
    return dump_schema(
        value,
        schema=schema,
        custom_dumpers={
            Message: dump_message,
        }
    )


def load(input: bytes, schema: Optional[Schema] = None) -> LoadedValue[Any]:
    """
    Loads service schema value, rpc call from data. uses custom loader for
    Message type

    Args:
        input - input bytes that should be loaded
        schema - common schema(where joined customer and service schema).
                 If schema not passed use only service_schema
    """
    if schema is None:
        schema = service_schema
    return load_schema(
        input,
        schema=schema,
        custom_loaders={
            Message: load_message,
        }
    )
