# -*- coding: utf-8 -*-
from contextlib import ExitStack
from unittest.mock import patch, MagicMock

import pytest

from mtpylon import Schema
from mtpylon.schema import CombinatorData, FunctionData
from mtpylon.exceptions import SchemaChangeError
from tests.simpleschema import (
    Bool,
    User,
    Task,
    TaskList,
    BoolTrue,
    register,
    login,
    set_task,
    get_task_list,
    schema
)
from tests.echoschema import (
    Reply,
    echo
)


class WrongCombinator:
    pass


def wrong_funcion():
    pass


@pytest.fixture
def one_schema():
    new_schema = Schema(
        constructors=[User, Bool],
        functions=[login, register],
    )
    return new_schema


@pytest.fixture
def another_schema():
    another_schema = Schema(
        constructors=[Reply],
        functions=[echo]
    )
    return another_schema


def test_schema():
    is_valid_constructor = MagicMock()
    is_valid_function = MagicMock()

    with ExitStack() as patcher:
        patcher.enter_context(patch(
            'mtpylon.schema.is_valid_constructor',
            is_valid_constructor
        ))
        patcher.enter_context(patch(
            'mtpylon.schema.is_valid_function',
            is_valid_function
        ))

        Schema(
            constructors=[
                Bool,
                User,
                Task,
                TaskList,
            ],
            functions=[
                register,
                login,
                set_task,
                get_task_list,
            ]
        )

    assert is_valid_constructor.called
    assert is_valid_constructor.call_count == 4
    assert is_valid_function.called
    assert is_valid_function.call_count == 4


def test_schema_structure():
    schema_structure = schema.get_schema_structure()

    constructor_predicates = [
        constructor.predicate
        for constructor in schema_structure.constructors
    ]

    function_names = [
        function.method
        for function in schema_structure.methods
    ]

    for predicate in [
        'boolTrue',
        'boolFalse',
        'authorizedUser',
        'anonymousUser',
        'task',
        'taskList'
    ]:
        assert predicate in constructor_predicates

    for method in [
        'register',
        'login',
        'set_task',
        'get_task_list',
    ]:
        assert method in function_names


def test_combinator_in_schema():
    assert BoolTrue in schema


def test_constructor_in_schema():
    assert Bool in schema


def test_function_in_schema():
    assert login in schema


def test_combinator_not_in_schema():
    assert WrongCombinator not in schema


def test_function_not_in_schema():
    assert wrong_funcion not in schema


def test_combinator_number_in_schema():
    assert 0x5d8fe2e9 in schema


def test_function_number_in_schema():
    assert 3391236435 in schema


def test_wrong_number():
    assert 32423 not in schema


def test_get_boolTrue_combinator_by_type():  # flake8: noqa
    combinator = schema[BoolTrue]
    assert isinstance(combinator, CombinatorData)
    assert combinator.id == 2574415285
    assert len(combinator.params) == 0
    assert combinator.predicate == 'boolTrue'
    assert combinator.type == 'Bool'


def test_get_task_combinator_by_type():
    combinator = schema[Task]
    assert isinstance(combinator, CombinatorData)
    assert combinator.id == 0xb801a563
    assert len(combinator.params) == 5
    assert combinator.predicate == 'task'
    assert combinator.type == 'Task'


def test_get_boolTrue_combinator_by_number():  # flake8: noqa
    combinator = schema[2574415285]
    assert isinstance(combinator, CombinatorData)
    assert combinator.id == 2574415285
    assert len(combinator.params) == 0
    assert combinator.predicate == 'boolTrue'
    assert combinator.type == 'Bool'


def test_get_task_combinator_by_number():
    combinator = schema[0xb801a563]
    assert isinstance(combinator, CombinatorData)
    assert combinator.id == 0xb801a563
    assert len(combinator.params) == 5
    assert combinator.predicate == 'task'
    assert combinator.type == 'Task'


def test_get_function_data_by_function():
    func = schema[login]
    assert isinstance(func, FunctionData)
    assert func.id == 475889219
    assert len(func.params) == 2
    assert func.method == 'login'
    assert func.type == 'User'


def test_get_function_data_by_number():
    func = schema[475889219]
    assert isinstance(func, FunctionData)
    assert func.id == 475889219
    assert len(func.params) == 2
    assert func.method == 'login'
    assert func.type == 'User'


def test_cant_get_construct():
    with pytest.raises(ValueError):
        schema[Bool]  # flake8: noqa


def test_key_error_combinator():
    with pytest.raises(KeyError):
        schema[WrongCombinator]  # flake8: noqa


def test_key_error_function():
    with pytest.raises(KeyError):
        schema[wrong_funcion]  # flake8: noqa


def test_key_error_number():
    with pytest.raises(KeyError):
        schema[12312]  # flake8: noqa


def test_schema_set_error():
    with pytest.raises(SchemaChangeError):
        schema[121312] = WrongCombinator


def test_schema_delete_error():
    with pytest.raises(SchemaChangeError):
        del schema[BoolTrue]


def test_schema_update_schema(one_schema, another_schema):
    one_schema.update(another_schema)

    assert Reply in one_schema
    assert echo in one_schema


def test_ior_update_schema(one_schema, another_schema):
    one_schema |= another_schema

    assert Reply in one_schema
    assert echo in one_schema


def test_or_create_schema(one_schema, another_schema):
    new_schema = one_schema | another_schema

    assert Bool in new_schema
    assert User in new_schema
    assert login in new_schema

    assert Reply in new_schema
    assert echo in new_schema


def test_duplicate_combinator(one_schema):
    simple_schema = Schema(constructors=[Bool], functions=[])

    with pytest.raises(ValueError):
        one_schema.update(simple_schema)


def test_duplicate_method(one_schema):
    simple_schema = Schema(constructors=[Bool, User], functions=[login])

    with pytest.raises(ValueError):
        one_schema.update(simple_schema)
