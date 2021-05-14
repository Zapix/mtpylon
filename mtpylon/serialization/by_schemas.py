# -*- coding: utf-8 -*-
from typing import List, Any, Optional

from mtpylon import Schema
from mtpylon.exceptions import DumpError
from mtpylon.serialization import (
    load as load_schema,
    dump as dump_schema,
    LoadedValue,
)


def dump(
    schemas: List[Schema],
    value: Any,
    **kwargs: Any
) -> bytes:
    """
    Dumps data by one of available schemas

    Raises:
        DumpError - if couldn't dump by one of schemas
    """
    result: Optional[bytes] = None

    for schema in schemas:
        try:
            result = dump_schema(schema, value, **kwargs)
        except DumpError:
            pass
        else:
            break

    if result is None:
        raise DumpError(f'Could not dump {value}')

    return result


def load(
    schemas: List[Schema],
    inputs: bytes,
) -> LoadedValue[Any]:
    """
    Loads data by one of available schemas

    Raises:
        ValueError - if could load by one of schemas
    """
    result: Any = None

    for schema in schemas:
        try:
            result = load_schema(schema, inputs)
        except ValueError:
            pass
        else:
            break

    if result is None:
        raise ValueError('Could not load bytes')

    return result
