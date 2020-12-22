# -*- coding: utf-8 -*-
import json

from mtpylon.serializers import (
    combinator_to_dict,
    function_to_dict,
    to_dict,
    to_json,
)

from .simpleschema import schema


combinator_names = [
    'boolTrue',
    'boolFalse',
    'authorizedUser',
    'anonymousUser',
    'task',
    'taskList',
]


type_names = [
    'Bool',
    'User',
    'Task',
    'TaskList',
]


method_names = [
  'register',
  'login',
  'set_task',
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
      "id": 1503360568,
      "predicate": "authorizedUser",
      "type": "User",
      "params": [
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
      "id": 6457282,
      "predicate": "task",
      "type": "Task",
      "params": [
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
    }
  ]
}


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
    schema_structure = schema.get_schema_structure()

    for combinator in schema_structure.constructors:
        combinator_data = combinator_to_dict(combinator)
        assert_combinator_data(combinator_data)


def test_function_to_dict():
    schema_structure = schema.get_schema_structure()

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
