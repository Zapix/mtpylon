# -*- coding: utf-8 -*-
from typing import Callable, Any

from mtpylon.serialization import LoadedValue
from mtpylon.serialization.int import dump as dump_int, load as load_int
from mtpylon.serialization.long import dump as dump_long, load as load_long

from ..constructors import RpcResult
from ..service_schema import service_schema


def dump(
    value: RpcResult,
    dump_result: Callable[[Any], bytes]
) -> bytes:
    data = service_schema[RpcResult]

    return (
        dump_int(data.id) +
        dump_long(value.req_msg_id) +
        dump_result(value.result)
    )


def load(
    input: bytes,
    load_result: Callable[[bytes], LoadedValue[Any]]
) -> LoadedValue[RpcResult]:
    data = service_schema[RpcResult]

    combinator = load_int(input[:4]).value

    if data.id != combinator:
        raise ValueError('Wrong Combinator passed')

    req_msg_id = load_long(input[4:]).value
    loaded_result = load_result(input[12:])

    return LoadedValue(
        value=RpcResult(
            req_msg_id=req_msg_id,
            result=loaded_result.value
        ),
        offset=12 + loaded_result.offset
    )
