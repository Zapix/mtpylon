# -*- coding: utf-8 -*-
from typing import overload, Any, Callable, Union, Dict
from functools import partial
from inspect import isfunction

from .bytes import dump as dump_bytes
from .int import dump as dump_int
from .long import dump as dump_long
from .int128 import dump as dump_int128
from .int256 import dump as dump_int256
from .double import dump as dump_double
from .string import dump as dump_string
from ..utils import long, int128, int256
from ..schema import Schema, FunctionData, CombinatorData
from ..exceptions import DumpError


DumpFunction = Callable[[Any], bytes]


@overload
def dump(schema: Schema, value: Any) -> bytes:
    ...


@overload
def dump(schema: Schema, value: Callable, **kwargs: Any) -> bytes:
    ...


def dump(schema, value, **kwargs):
    """
    Dumps basic or boxed types by schema
    """
    def dump_by_type(
            value: Any,
            param: Union[FunctionData, CombinatorData]
    ) -> bytes:
        dump_map: Dict[Any, DumpFunction] = {
            int: dump_int,
            long: dump_long,
            int128: dump_int128,
            int256: dump_int256,
            float: dump_double,
            bytes: dump_bytes,
            str: dump_string
        }
        dump_func: DumpFunction = dump_map.get(
            param.origin,
            partial(dump, schema)
        )
        try:
            dumped = dump_func(value)
        except Exception:
            raise DumpError(f'Can`t dump {value} as f{param.type}')
        return dumped

    if isfunction(value):
        try:
            data = schema[value]
        except KeyError:
            raise DumpError('Can`t dump function that not in schema')

        dumped = b''.join(
            [dump_int(data.id)] +
            [
                dump_by_type(kwargs[param.name], param)
                for param in data.params
            ]
        )
    else:
        try:
            data = schema[type(value)]
        except KeyError:
            raise DumpError('Can`t dump combinator that not in schema')

        dumped = b''.join(
            [dump_int(data.id)] +
            [
                dump_by_type(getattr(value, param.name), param)
                for param in data.params
            ]
        )

    return dumped
