# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import (
    cast,
    overload,
    Any,
    Callable,
    Union,
    Dict,
    Optional,
    List,
    Type,
    NamedTuple,
)
from functools import partial
from inspect import isfunction

from .bytes import dump as dump_bytes, load as load_bytes
from .int import dump as dump_int, load as load_int
from .long import dump as dump_long, load as load_long
from .int128 import dump as dump_int128, load as load_int128
from .int256 import dump as dump_int256, load as load_int256
from .double import dump as dump_double, load as load_double
from .string import dump as dump_string, load as load_string
from .vector import dump as dump_vector, load as load_vector
from .object import dump as dump_object, load as load_object
from .loaded import LoadedValue
from ..utils import (
    is_list_type,
    is_optional_type,
    AttrDescription,
)
from .. import long, int128, int256
from ..schema import Schema, FunctionData, CombinatorData
from ..exceptions import DumpError


DumpFunction = Callable[[Any], bytes]
LoadFunction = Callable[[bytes], LoadedValue[Any]]

CustomDumpersMap = Dict[Any, DumpFunction]
CustomLoadersMap = Dict[Any, LoadFunction]


@dataclass
class CallableFunc:
    func: Callable
    params: Dict[str, Any]


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


def get_flag_value(flag_number: int, param_name: str, origin: Type) -> int:
    """
    Get flag value by param name
    """
    return (flag_number >> get_flag_ids(origin, param_name)) & 1


def set_flag_value(flag_number: int, param_name: str, origin: Type) -> int:
    """
    Updates flag value and returns it
    """
    return flag_number | (1 << get_flag_ids(origin, param_name))


@overload
def dump(
        schema: Schema,
        value: Any,
        custom_dumpers: Optional[CustomDumpersMap],
) -> bytes:
    ...


@overload
def dump(
        schema: Schema,
        value: Callable,
        custom_dumpers: Optional[CustomDumpersMap],
        **kwargs: Any,
) -> bytes:
    ...


def dump(schema, value, custom_dumpers=None, **kwargs):
    """
    Dumps basic or boxed types by schema
    """
    if custom_dumpers is None:
        custom_dumpers = {}

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
            str: dump_string,
            Any: dump_object,
        }
        dump_map.update(custom_dumpers)

        try:
            if is_list_type(origin):
                item_origin = origin.__args__[0]
                dump_item: DumpFunction = dump_map.get(
                    item_origin,
                    partial(dump, schema, custom_dumpers=custom_dumpers)
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

    if type(value) in custom_dumpers:
        dump_function = custom_dumpers[type(value)]
        return dump_function(value)

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
            flags_value = set_flag_value(flags_value, param.name, data.origin)
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


def load(
        schema: Schema,
        input: bytes,
        custom_loaders: Optional[CustomLoadersMap] = None
) -> LoadedValue[Union[CallableFunc, Any]]:
    """
    Loads object or function with params from bytes input

    Args:
        schema - schema that will be used to load
        input - serialized value

    Raises:
        ValueError - when can't load data
    """
    if custom_loaders is None:
        custom_loaders = {}

    def load_empty(x: bytes) -> LoadedValue[None]:
        return LoadedValue(None, 0)

    load_map = {
        bytes: load_bytes,
        int: load_int,
        long: load_long,
        int128: load_int128,
        int256: load_int256,
        float: load_double,
        str: load_string,
        Any: load_object,
        type(None): load_empty,
    }
    load_map.update(custom_loaders)

    def get_load_func(x) -> LoadFunction:
        return load_map.get(
            x,
            partial(load, schema, custom_loaders=custom_loaders)
        )

    offset = 0
    loaded_combinator = load_int(input)
    offset += loaded_combinator.offset
    combinator = loaded_combinator.value

    if combinator not in schema:
        raise ValueError(f'Can`t find combinator {combinator} in schema')

    data = schema[combinator]

    if isinstance(data.origin, type) and data.origin in custom_loaders:
        loader = custom_loaders[data.origin]
        return loader(input)

    flag_number: Optional[int] = None
    params: Dict[str, Any] = {}

    for param in data.params:
        if param.name == 'flags':
            loaded = load_int(input[offset:])
            flag_number = loaded.value
            offset += loaded.offset
            continue

        origin = param.origin
        if is_optional_type(origin) and flag_number is not None:
            if get_flag_value(
                    flag_number,
                    param.name,
                    cast(Type, data.origin),
            ):
                origin = origin.__args__[0]
            else:
                origin = type(None)

        if is_list_type(origin):
            load_item_func: Callable[[bytes], LoadedValue[Any]] = (
                get_load_func(origin.__args__[0])
            )
            load_func: Callable[[bytes], LoadedValue[Any]] = (
                partial(load_vector, load_item_func)
            )
        else:
            load_func = get_load_func(origin)

        loaded = load_func(input[offset:])
        params[param.name] = loaded.value
        offset += loaded.offset

    if isfunction(data.origin):
        value = CallableFunc(data.origin, params)
    else:
        value = data.origin(**params)

    return LoadedValue(value=value, offset=offset)
