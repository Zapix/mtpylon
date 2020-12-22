# -*- coding: utf-8 -*-
from contextlib import ExitStack
from unittest.mock import patch, MagicMock

from mtpylon import Schema
from tests.simpleschema import Bool, User, Task, TaskList, register, login, \
    set_task, get_task_list, schema


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
