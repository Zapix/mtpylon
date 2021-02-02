# -*- coding: utf-8 -*-
from contextlib import ExitStack
from unittest.mock import patch, MagicMock

from mtpylon import Schema
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


class WrongCombinator:
    pass


def wrong_funcion():
    pass


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
    assert 1503360568 in schema


def test_function_number_in_schema():
    assert 3391236435 in schema


def test_wrong_number():
    assert 32423 not in schema
