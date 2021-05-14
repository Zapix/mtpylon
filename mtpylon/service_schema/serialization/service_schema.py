# -*- coding: utf-8 -*-
from typing import Any, Optional, List
from functools import partial

from mtpylon.serialization import (
    load as load_schema,
    dump as dump_schema,
    LoadedValue,
)
from mtpylon.schema import Schema

from ..service_schema import service_schema
from ..constructors import Message, RpcResult
from .message import dump as dump_message, load as load_message
from ...serialization.by_schemas import (
    dump as dump_by_schemas,
    load as load_by_schemas
)
from .rpc_result import (
    dump as dump_rpc_result,
    load as load_rpc_result
)


def build_available_schemas(schema: Optional[Schema]) -> List[Schema]:
    schemas = [
        service_schema
    ]

    if schema is not None:
        schemas.append(schema)

    return schemas


def dump(value: Any, schema: Optional[Schema] = None, **kwargs: Any) -> bytes:
    """
    Dumps service schema values, rpc calls. Uses custom dumper for
    Message type
    """
    return dump_schema(
        service_schema,
        value,
        custom_dumpers={
            Message: dump_message,
            RpcResult: partial(
                dump_rpc_result,
                dump_result=partial(
                    dump_by_schemas,
                    build_available_schemas(schema),
                )
            ),
        },
        **kwargs
    )


def load(input: bytes, schema: Optional[Schema] = None) -> LoadedValue[Any]:
    """
    Loads service schema value, rpc call from data. uses custom loader for
    Message type
    """
    return load_schema(
        service_schema,
        input,
        custom_loaders={
            Message: load_message,
            RpcResult: partial(
                load_rpc_result,
                load_result=partial(
                    load_by_schemas,
                    build_available_schemas(schema)
                )
            )
        }
    )
