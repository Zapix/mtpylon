# -*- coding: utf-8 -*-
import json

from mtpylon.serializers import (
    combinator_to_dict,
    function_to_dict,
    to_dict,
    to_json,
    combinator_to_tl,
    function_to_tl,
    to_tl_program,
    FUNCTIONS_SEPARATOR
)

from .simpleschema import schema

combinator_names = [
    'boolTrue',
    'boolFalse',
    'authorizedUser',
    'anonymousUser',
    'task',
    'taskList',
    'entity_comment',
]

type_names = [
    'Bool',
    'User',
    'Task',
    'TaskList',
    'EntityComment',
]

method_names = [
    'register',
    'login',
    'set_task',
    'get_task',
    'get_task_list',
]

json_schema = {
    "constructors": [
        {
            "id": 2574415285,
            "predicate": "boolTrue",
            "type": "Bool",
            "params": []
        },
        {
            "id": 3162085175,
            "predicate": "boolFalse",
            "type": "Bool",
            "params": []
        },
        {
            "id": 0x5d8fe2e9,
            "predicate": "authorizedUser",
            "type": "User",
            "params": [
                {
                    "name": "flags",
                    "type": "#"
                },
                {
                    "name": "id",
                    "type": "int"
                },
                {
                    "name": "username",
                    "type": "string"
                },
                {
                    "name": "password",
                    "type": "string"
                },
                {
                    'name': 'avatar_url',
                    'type': 'flags.0?string'
                }
            ]
        },
        {
            "id": 1563593667,
            "predicate": "anonymousUser",
            "type": "User",
            "params": []
        },
        {
            "id": 0xb801a563,
            "predicate": "task",
            "type": "Task",
            "params": [
                {
                    'name': 'flags',
                    'type': '#'
                },
                {
                    "name": "id",
                    "type": "int"
                },
                {
                    "name": "content",
                    "type": "string"
                },
                {
                    "name": "completed",
                    "type": "Bool"
                },
                {
                    "name": "tags",
                    "type": "flags.1?Vector<string>"
                }
            ]
        },
        {
            "id": 1721237574,
            "predicate": "taskList",
            "type": "TaskList",
            "params": [
                {
                    "name": "tasks",
                    "type": "Vector<Task>"
                }
            ]
        },
        {
            "id": 3098825498,
            "predicate": "entity_comment",
            "type": "EntityComment",
            "params": [
                {
                    "name": "entity",
                    "type": "Object",
                },
                {
                    "name": "comment",
                    "type": "string"
                }
            ]
        }
    ],
    "methods": [
        {
            "id": 2043668814,
            "method": "register",
            "type": "User",
            "params": [
                {
                    "name": "username",
                    "type": "string"
                },
                {
                    "name": "password",
                    "type": "string"
                }
            ]
        },
        {
            "id": 475889219,
            "method": "login",
            "type": "User",
            "params": [
                {
                    "name": "username",
                    "type": "string"
                },
                {
                    "name": "password",
                    "type": "string"
                }
            ]
        },
        {
            "id": 225927515,
            "method": "set_task",
            "type": "Task",
            "params": [
                {
                    "name": "content",
                    "type": "string"
                }
            ]
        },
        {
            "id": 3391236435,
            "method": "get_task_list",
            "type": "TaskList",
            "params": []
        },
        {
            "id": 3370625417,
            "method": "get_task",
            "type": "Task",
            "params": [
                {
                    "name": "task_id",
                    "type": "int",
                },
            ],
        },
    ]
}

tl_combinators = [
    'boolTrue#997275b5 = Bool;',
    'boolFalse#bc799737 = Bool;',
    'authorizedUser#5d8fe2e9 flags:# id:int username:string password:string avatar_url:flags.0?string = User;',  # noqa: E501
    'anonymousUser#5d328bc3 = User;',
    'task#b801a563 flags:# id:int content:string completed:Bool tags:flags.1?Vector<string> = Task;',  # noqa: E501
    'taskList#66980046 tasks:Vector<Task> = TaskList;',
    'entity_comment#b8b4531a entity:Object comment:string = EntityComment;',
]

tl_methods = [
    'register#79cfe94e username:string password:string = User;',
    'login#1c5d7e43 username:string password:string = User;',
    'set_task#0d77615b content:string = Task;',
    'get_task_list#ca222953 = TaskList;',
    'get_task#c8e7a989 task_id:int = Task;',
]

tl_program = tl_combinators + [FUNCTIONS_SEPARATOR] + tl_methods

schema_structure = schema.get_schema_structure()


def assert_combinator_data(combinator_data: dict) -> None:
    assert 'id' in combinator_data
    assert 'predicate' in combinator_data
    assert 'params' in combinator_data
    assert 'type' in combinator_data

    assert isinstance(combinator_data['id'], int)

    assert combinator_data['predicate'] in combinator_names

    assert combinator_data['type'] in type_names

    assert isinstance(combinator_data['params'], list)
    for param in combinator_data['params']:
        assert 'name' in param
        assert 'type' in param


def assert_function_data(function_data: dict) -> None:
    assert 'id' in function_data
    assert 'method' in function_data
    assert 'params' in function_data
    assert 'type' in function_data

    assert isinstance(function_data['id'], int)

    assert function_data['method'] in method_names

    assert function_data['type'] in type_names

    assert isinstance(function_data['params'], list)
    for param in function_data['params']:
        assert 'name' in param
        assert 'type' in param


def test_combinator_to_dict():
    for combinator in schema_structure.constructors:
        combinator_data = combinator_to_dict(combinator)
        assert_combinator_data(combinator_data)


def test_function_to_dict():
    for method in schema_structure.methods:
        function_data = function_to_dict(method)
        assert_function_data(function_data)


def test_to_dict():
    jsonable = to_dict(schema)

    assert 'constructors' in jsonable
    for combinator_data in jsonable['constructors']:
        assert_combinator_data(combinator_data)

    assert 'methods' in jsonable
    for method in jsonable['methods']:
        assert_function_data(method)

    assert jsonable == json_schema


def test_to_json():
    assert to_json(schema) == json.dumps(json_schema)


def test_combinator_to_tl():
    for combinator in schema_structure.constructors:
        combinator_str = combinator_to_tl(combinator)
        assert combinator_str in tl_combinators


def test_function_to_tl():
    for method in schema_structure.methods:
        method_str = function_to_tl(method)
        assert method_str in tl_methods


def test_to_tl_program():
    assert to_tl_program(schema) == '\n'.join(tl_program)
