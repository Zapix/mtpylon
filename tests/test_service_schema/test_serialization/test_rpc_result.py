# -*- coding: utf-8 -*-
import pytest
from functools import partial

from mtpylon import long
from mtpylon.service_schema.constructors import RpcResult, RpcError
from mtpylon.serialization import (
    load as load_schema,
    dump as dump_schema
)
from mtpylon.service_schema.serialization.rpc_result import (
    dump as dump_rpc_result,
    load as load_rpc_result
)
from mtpylon.service_schema import service_schema

from tests.echoschema import schema, Reply


rpc_result_error_bytes = (
    b'\x01m\\\xf3' +
    b'\x00\x00\x00\x00\np\x0b^' +
    b'\x19\xcaD!\x94\x01\x00\x00\tNot Found\x00\x00'
)

rpc_result_error = RpcResult(
    req_msg_id=long(0x5e0b700a00000000),
    result=RpcError(
        error_code=404,
        error_message='Not Found',
    ),
)


rpc_result_reply_bytes = (
    b'\x01m\\\xf3' +
    b'\x00\x00\x00\x00\np\x0b^' +
    b'>\x00j\r,\x00\x00\x00\x0bhello world'
)

rpc_result_reply = RpcResult(
    req_msg_id=long(0x5e0b700a00000000),
    result=Reply(
        content='hello world',
        rand_id=44,
    ),
)


def test_dump_rpc_error():
    assert dump_rpc_result(
        rpc_result_error,
        partial(dump_schema, service_schema)
    ) == rpc_result_error_bytes


def test_load_rpc_error():
    loaded = load_rpc_result(
        rpc_result_error_bytes,
        partial(load_schema, service_schema)
    )

    assert loaded.value == rpc_result_error
    assert loaded.offset == len(rpc_result_error_bytes)


def test_dump_rpc_reply():

    assert dump_rpc_result(
        rpc_result_reply,
        partial(dump_schema, schema)
    ) == rpc_result_reply_bytes


def test_load_rpc_reply():
    loaded = load_rpc_result(
        rpc_result_reply_bytes,
        partial(load_schema, schema)
    )

    assert loaded.value == rpc_result_reply
    assert loaded.offset == len(rpc_result_reply_bytes)


def test_load_rpc_raise_value_error():
    with pytest.raises(ValueError):
        load_rpc_result(
            rpc_result_reply_bytes[4:],
            partial(load_schema, schema)
        )
