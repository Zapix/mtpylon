# -*- coding: utf-8 -*-
import pytest

from mtpylon.exceptions import DumpError
from mtpylon.serialization.by_schemas import (
    load as load_by_schemas,
    dump as dump_by_schemas
)
from mtpylon.service_schema import service_schema
from mtpylon.service_schema.constructors import RpcError

rpc_error_bytes = b'\x19\xcaD!\x94\x01\x00\x00\tNot Found\x00\x00'

rpc_error = RpcError(
    error_code=404,
    error_message='Not Found',
)


def test_load_message():
    loaded = load_by_schemas([service_schema], rpc_error_bytes)
    assert loaded.value == rpc_error


def test_dump_message():
    dumped_bytes = dump_by_schemas([service_schema], rpc_error)
    assert rpc_error_bytes == dumped_bytes


def test_load_error():
    with pytest.raises(ValueError):
        load_by_schemas([], rpc_error_bytes)


def test_dump_error():
    with pytest.raises(DumpError):
        dump_by_schemas([], rpc_error)
