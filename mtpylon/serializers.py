# -*- coding: utf-8 -*-
import json
from typing import List

from .utils import AttrDescription
from .schema import Schema, CombinatorData, FunctionData

FUNCTIONS_SEPARATOR = '---functions---'


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


def attr_description_to_tl(attr: AttrDescription) -> str:
    """
    Dumps attr description to string

    Args:
        attr - attribute description that should be dumped
    """
    return f'{attr.name}:{attr.type}'


def params_to_tl(params: List[AttrDescription]) -> str:
    if not params:
        return ''

    return ' '.join([
        attr_description_to_tl(attr) for attr in params
    ] + [''])


def combinator_to_tl(combinator: CombinatorData) -> str:
    """
    Dumps combinator_data to tl_program string

    Args:
        combinator - combinator data that should be dumped
    """
    return '{predicate}#{id} {params}= {type};'.format(**{
        'predicate': combinator.predicate,
        'id': f'{combinator.id:08x}',
        'params': params_to_tl(combinator.params),
        'type': combinator.type
    })


def function_to_tl(func: FunctionData) -> str:
    """
    Dumps functions_data to tl_program string

    Args:
        func - function data that should be dumped
    """
    return '{method}#{id} {params}= {type};'.format(**{
        'method': func.method,
        'id': f'{func.id:08x}',
        'params': params_to_tl(func.params),
        'type': func.type
    })


def to_tl_program(schema: Schema) -> str:
    """
    Dumps schema as tl program. Pls check:
    https://core.telegram.org/mtproto/TL

    Args:
        schema - valid schema
    """
    schema_structure = schema.get_schema_structure()
    program_str = [
        combinator_to_tl(combinator)
        for combinator in schema_structure.constructors
    ] + [
        FUNCTIONS_SEPARATOR
    ] + [
        function_to_tl(method)
        for method in schema_structure.methods
    ]
    return '\n'.join(program_str)
