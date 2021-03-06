# -*- coding: utf-8 -*-
from typing import no_type_check

import pytest

from mtpylon.serialization import dump, load
from mtpylon.serialization.schema import CallableFunc
from mtpylon.exceptions import DumpError
from mtpylon.serialization.loaded import LoadedValue

from ..simpleschema import (
    schema,
    BoolTrue,
    BoolFalse,
    Task,
    TaskList,
    AuthorizedUser,
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
        completed=BoolTrue(),
        tags=None
    )

    assert dump(schema, task) == (
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
    )


def test_dump_task_object_with_tags():
    task = Task(
        id=12,
        content='dump by schema',
        completed=BoolTrue(),
        tags=['schema', 'dump']
    )

    assert dump(schema, task) == (
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x02\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x02\x00\x00\x00' +  # vector size
        b'\x06schema\x00' +  # tag 'schema'
        b'\x04dump\x00\x00\x00'  # tag 'dump
    )


def test_dump_authroized_user_with_optional_field():
    authorized_user = AuthorizedUser(
        id=12,
        username='zapix',
        password='123123',
        avatar_url='http://example.com/1.jpg'
    )
    assert dump(schema, authorized_user) == (
        b'\xe9\xe2\x8f\x5d' +  # combinator id
        b'\x01\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # user id
        b'\x05zapix\x00\x00' +  # username
        b'\x06123123\x00' +  # password
        b'\x18http://example.com/1.jpg\x00\x00\x00'
    )


def test_dump_authorized_user_without_optional_field():
    authorized_user = AuthorizedUser(
        id=12,
        username='zapix',
        password='123123',
        avatar_url=None,
    )
    assert dump(schema, authorized_user) == (
        b'\xe9\xe2\x8f\x5d' +  # combinator id
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # user id
        b'\x05zapix\x00\x00' +  # username
        b'\x06123123\x00'  # password
    )


def test_dump_task_list():
    task_list = TaskList(
        tasks=[
            Task(
                id=12,
                content='dump by schema',
                completed=BoolTrue(),
                tags=None,
            ),
            Task(
                id=16,
                content='dump list',
                completed=BoolFalse(),
                tags=None,
            )
        ]
    )
    assert dump(schema, task_list) == (
        b'\x46\x00\x98\x66' +  # combinator id
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x02\x00\x00\x00' +  # vector size
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x10\x00\x00\x00' +  # id number - int
        b'\x09dump list\x00\x00' +  # content - str
        b'\x37\x97\x79\xbc'  # completed - Bool
    )


def test_dump_get_task_list_function():
    assert dump(schema, get_task_list) == b'S)"\xca'


def test_dump_login_function():
    assert dump(schema, login, username='root', password='root') == (
        b'C~]\x1c' +  # function login
        b'\x04root\x00\x00\x00' +  # username
        b'\x04root\x00\x00\x00'  # password
    )


def test_dump_custom_bool():
    def dump_custom_bool_true(value):
        return b'\xb5\x75\x72\x99' + b'custom'

    def dump_custom_bool_false(value):
        return b'\x37\x97\x79\xbc' + b'custom'

    custom_dumpers = {
        BoolTrue: dump_custom_bool_true,
        BoolFalse: dump_custom_bool_false
    }

    dumped_true = dump(schema, BoolTrue(), custom_dumpers=custom_dumpers)
    assert dumped_true == b'\xb5\x75\x72\x99' + b'custom'

    dumped_false = dump(schema, BoolFalse(), custom_dumpers=custom_dumpers)
    assert dumped_false == b'\x37\x97\x79\xbc' + b'custom'


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
    task = Task(id=12, content=12312, completed=BoolFalse(), tags=None)
    with pytest.raises(DumpError):
        dump(schema, task)


def test_load_bool_true():
    input = b'\xb5\x75\x72\x99'
    loaded = load(schema, input)
    assert loaded.value == BoolTrue()
    assert loaded.offset == 4


def test_load_bool_false():
    input = b'\x37\x97\x79\xbc'
    loaded = load(schema, input)
    assert loaded.value == BoolFalse()
    assert loaded.offset == 4


def test_load_task():
    input = (
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
    )

    loaded = load(schema, input)
    assert isinstance(loaded.value, Task)
    assert loaded.value.id == 12
    assert loaded.value.content == 'dump by schema'
    assert loaded.value.completed == BoolTrue()
    assert loaded.offset == 32


def test_load_task_with_tags():
    input = (
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x02\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x02\x00\x00\x00' +  # vector size
        b'\x06schema\x00' +  # tag 'schema'
        b'\x04dump\x00\x00\x00'  # tag 'dump
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, Task)
    assert loaded.value.id == 12
    assert loaded.value.content == 'dump by schema'
    assert loaded.value.completed == BoolTrue()
    assert len(loaded.value.tags) == 2
    assert 'schema' in loaded.value.tags
    assert 'dump' in loaded.value.tags
    assert loaded.offset == 56


def test_load_authorized_user_with_avatar_url():
    input = (
        b'\xe9\xe2\x8f\x5d' +  # combinator id
        b'\x01\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # user id
        b'\x05zapix\x00\x00' +  # username
        b'\x06123123\x00' +  # password
        b'\x18http://example.com/1.jpg\x00\x00\x00'
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, AuthorizedUser)
    assert loaded.value.id == 12
    assert loaded.value.username == 'zapix'
    assert loaded.value.password == '123123'
    assert loaded.value.avatar_url == 'http://example.com/1.jpg'
    assert loaded.offset == 56


def test_load_authorized_user_without_avatar_url():
    input = (
        b'\xe9\xe2\x8f\x5d' +  # combinator id
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # user id
        b'\x05zapix\x00\x00' +  # username
        b'\x06123123\x00'  # password
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, AuthorizedUser)
    assert loaded.value.id == 12
    assert loaded.value.username == 'zapix'
    assert loaded.value.password == '123123'
    assert loaded.offset == 28


def test_load_task_list():
    input = (
        b'\x46\x00\x98\x66' +  # combinator id
        b'\x15\xc4\xb5\x1c' +  # vector id
        b'\x02\x00\x00\x00' +  # vector size
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x0c\x00\x00\x00' +  # id number - int
        b'\x0edump by schema\x00' +  # content - str
        b'\xb5\x75\x72\x99'  # completed - Bool
        b'\x63\xa5\x01\xb8' +  # task combinator number
        b'\x00\x00\x00\x00' +  # flags
        b'\x10\x00\x00\x00' +  # id number - int
        b'\x09dump list\x00\x00' +  # content - str
        b'\x37\x97\x79\xbc'  # completed - Bool
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, TaskList)
    assert len(loaded.value.tasks) == 2
    assert loaded.offset == 72


def test_load_get_task_list():
    input = (
        b'S)"\xca'
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, CallableFunc)
    assert loaded.value.func == get_task_list
    assert loaded.value.params == {}
    assert loaded.offset == 4


def test_load_login_func():
    input = (
        b'C~]\x1c' +  # function login
        b'\x04root\x00\x00\x00' +  # username
        b'\x04root\x00\x00\x00'  # password
    )

    loaded = load(schema, input)

    assert isinstance(loaded.value, CallableFunc)
    assert loaded.value.func == login
    assert loaded.value.params['username'] == 'root'
    assert loaded.value.params['password'] == 'root'
    assert loaded.offset == 20


def test_custom_loaders():
    dumped_true = b'\xb5\x75\x72\x99' + b'custom'
    dumped_false = b'\x37\x97\x79\xbc' + b'custom'

    def bool_true_loader(input: bytes) -> LoadedValue[BoolTrue]:
        return LoadedValue(BoolTrue(), offset=10)

    def bool_false_loader(input: bytes) -> LoadedValue[BoolFalse]:
        return LoadedValue(BoolFalse(), offset=10)

    custom_loaders = {
        BoolTrue: bool_true_loader,
        BoolFalse: bool_false_loader,
    }
    loaded = load(schema, dumped_true, custom_loaders=custom_loaders)

    assert loaded.value == BoolTrue()
    assert loaded.offset == 10

    loaded = load(schema, dumped_false, custom_loaders=custom_loaders)

    assert loaded.value == BoolFalse()
    assert loaded.offset == 10


def test_no_value():
    input = (
        b'\x01\x00\x00\x00'
    )

    with pytest.raises(ValueError):
        load(schema, input)
