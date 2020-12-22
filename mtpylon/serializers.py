# -*- coding: utf-8 -*-
import json

from .schema import Schema, CombinatorData, FunctionData


def combinator_to_dict(combinator: CombinatorData) -> dict:
    return {
        'id': combinator.id,
        'predicate': combinator.predicate,
        'type': combinator.type,
        'params': [
            {
                'name': param.name,
                'type': param.type,
            }
            for param in combinator.params
        ],
    }


def function_to_dict(func: FunctionData) -> dict:
    return {
        'id': func.id,
        'method': func.method,
        'type': func.type,
        'params': [
            {
                'name': param.name,
                'type': param.type,
            }
            for param in func.params
        ]
    }


def to_dict(schema: Schema) -> dict:
    """
    Dumps schema to jsonable dict.

    Args:
        schema - valid mtproto schema
    """
    schema_structure = schema.get_schema_structure()
    return {
        'constructors': [
            combinator_to_dict(combinator)
            for combinator in schema_structure.constructors
        ],
        'methods': [
            function_to_dict(method)
            for method in schema_structure.methods
        ],
    }


def to_json(schema: Schema) -> str:
    return json.dumps(to_dict(schema))
