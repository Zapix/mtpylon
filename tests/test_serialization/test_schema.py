# -*- coding: utf-8 -*-
from typing import no_type_check

import pytest

from mtpylon.serialization import dump
from mtpylon.exceptions import DumpError

from ..simpleschema import (
    schema,
    BoolTrue,
    BoolFalse,
    Task,
    get_task_list,
    login
)


class WrongObject:
    pass


def wrong_function():
    pass


def test_dump_bool_true():
    assert dump(schema, BoolTrue()) == b'\xb5\x75\x72\x99'


def test_dump_bool_false():
    assert dump(schema, BoolFalse()) == b'\x37\x97\x79\xbc'


def test_dump_task_object():
    task = Task(
        id=12,
        content='dump by schema',
        completed=BoolTrue()
    )

    assert dump(schema, task) == (
        b'\xc2\x87b\x00' +  # task combinator number
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
    )


def test_dump_get_task_list_function():
    assert dump(schema, get_task_list) == b'S)"\xca'


def test_dump_login_function():
    assert dump(schema, login, username='root', password='root') == (
        b'C~]\x1c' +  # function login
        b'\x04root\x00\x00\x00' +  # username
        b'\x04root\x00\x00\x00'  # password
    )


def test_dump_wrong_object():
    obj = WrongObject()
    with pytest.raises(DumpError):
        dump(schema, obj)


def test_dump_wrong_function():
    with pytest.raises(DumpError):
        dump(schema, wrong_function)


def test_wrong_function_params():
    with pytest.raises(DumpError):
        dump(schema, login, username='root', password=123)


@no_type_check
def test_dump_wrong_object_params():
    task = Task(id=12, content=12312, completed=BoolFalse())
    with pytest.raises(DumpError):
        dump(schema, task)
