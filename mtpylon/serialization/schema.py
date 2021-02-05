# -*- coding: utf-8 -*-
from typing import (
    overload,
    Any,
    Callable,
    Union,
    Dict,
    Optional,
    List,
    Type,
    NamedTuple
)
from functools import partial
from inspect import isfunction

from .bytes import dump as dump_bytes
from .int import dump as dump_int
from .long import dump as dump_long
from .int128 import dump as dump_int128
from .int256 import dump as dump_int256
from .double import dump as dump_double
from .string import dump as dump_string
from .vector import dump as dump_vector
from ..utils import (
    long,
    int128,
    int256,
    is_list_type,
    AttrDescription,
)
from ..schema import Schema, FunctionData, CombinatorData
from ..exceptions import DumpError


DumpFunction = Callable[[Any], bytes]


class Value2Dump(NamedTuple):
    value: Any
    param: AttrDescription


def get_flag_ids(origin: Type, param_name: str) -> int:
    """
    Get flag index for combinator

    Args:
        origin - type of origin comibnator
        param_name - name of param
    """
    flags = origin.Meta.flags
    return flags[param_name]


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
            dump_value: Any,
            origin: Type,
            type_name: str,
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

        try:
            if is_list_type(origin):
                item_origin = origin.__args__[0]
                dump_item: DumpFunction = dump_map.get(
                    item_origin,
                    partial(dump, schema)
                )
                return dump_vector(dump_item, dump_value)
            else:
                dump_func: DumpFunction = dump_map.get(
                    origin,
                    partial(dump, schema)
                )
                return dump_func(dump_value)
        except Exception:
            raise DumpError(f'Can`t dump {value} as {type_name}')

    data: Optional[Union[CombinatorData, FunctionData]] = None
    values_2_dump: List[Value2Dump] = []

    dumped_values: List[bytes] = []
    flags: Dict[str, int] = {}
    flags_value: Optional[int] = None

    if isfunction(value):
        try:
            data = schema[value]
        except KeyError:
            raise DumpError('Can`t dump function that not in schema')

        values_2_dump = [
            Value2Dump(kwargs.get(param.name), param)
            for param in data.params
        ]
    else:
        try:
            data = schema[type(value)]
        except KeyError:
            raise DumpError('Can`t dump combinator that not in schema')

        flags = getattr(data.origin.Meta, 'flags', {})

        values_2_dump = [
            Value2Dump(getattr(value, param.name, None), param)
            for param in data.params
        ]

    for item in values_2_dump:
        attr_value = item.value
        param = item.param

        if param.name == 'flags':
            flags_value = 0
            continue

        if param.name in flags:
            if attr_value is None:
                continue
            origin = param.origin.__args__[0]
            type_name = param.type
            flags_value |= 1 << get_flag_ids(data.origin, param.name)
        else:
            origin = param.origin
            type_name = param.type

        dumped_values.append(dump_by_type(attr_value, origin, type_name))

    dumped_flag = dump_int(flags_value) if flags_value is not None else b''

    dumped = b''.join(
        [
            dump_int(data.id),
            dumped_flag
        ] +
        dumped_values
    )
    return dumped
