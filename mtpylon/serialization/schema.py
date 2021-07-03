# -*- coding: utf-8 -*-
from dataclasses import dataclass, Field
from typing import (
    cast,
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
from inspect import isfunction, signature
from mypy_extensions import Arg, NamedArg

from .bytes import dump as dump_bytes, load as load_bytes
from .int import dump as dump_int, load as load_int
from .long import dump as dump_long, load as load_long
from .int128 import dump as dump_int128, load as load_int128
from .int256 import dump as dump_int256, load as load_int256
from .double import dump as dump_double, load as load_double
from .string import dump as dump_string, load as load_string
from .vector import dump as dump_vector, load as load_vector
from .loaded import LoadedValue
from ..utils import (
    is_list_type,
    is_optional_type,
    get_fields_map,
    AttrDescription,
)
from .. import long, int128, int256
from ..schema import Schema, FunctionData, CombinatorData
from ..exceptions import DumpError


DumpBasicTypeFunction = Callable[[Any], bytes]
DumpFunction = Callable[
    [
        Any,
        Arg(bool, 'bare')  # noqa: F821
    ],
    bytes
]
DumpFunctionWithDumpObject = Callable[
    [
        Any,
        NamedArg(bool, 'bare'),  # noqa: F821
        NamedArg(DumpFunction, 'dump_object')  # noqa: F821
    ],
    Any
]

LoadBasicTypeFunction = Callable[[bytes], LoadedValue[Any]]
LoadFunction = Callable[
    [
        bytes,
        NamedArg(bool, 'bare')  # noqa: F821
    ],
    LoadedValue[Any]
]
LoadFunctionWithLoadObject = Callable[
    [
        Any,
        NamedArg(bool, 'bare'),  # noqa: F821
        NamedArg(LoadFunction, 'load_object')  # noqa: F821
    ],
    LoadedValue[Any]
]

CustomDumpFunction = Union[DumpFunction, DumpFunctionWithDumpObject]
CustomLoadFunction = Union[LoadFunction, LoadFunctionWithLoadObject]

BasicTypeDumpers = Dict[Any, DumpBasicTypeFunction]
BasicTypeLoaders = Dict[Any, LoadBasicTypeFunction]

DumpersMap = Dict[Any, DumpFunction]
LoadersMap = Dict[Any, LoadFunction]

CustomDumpersMap = Dict[Any, CustomDumpFunction]
CustomLoadersMap = Dict[Any, CustomLoadFunction]


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
    fields_map = get_fields_map(origin)
    field = fields_map[param_name]
    return field.metadata['flag']


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


def is_bare_field(field: Optional[Field]):
    """
    Checks should we dump param as bare type or not
    """
    if field is None:
        return False

    return 'bare' in field.metadata


def is_bare_item_field(field: Optional[Field]):
    if field is None:
        return False

    return 'bare' in field.metadata.get('item_meta', {})


def build_custom_dumper_func(
    func: CustomDumpFunction,
    dump_object: DumpFunction
) -> DumpFunction:
    """
    Pass object dump function if it required
    """
    sig = signature(func)

    if 'dump_object' in sig.parameters:
        func = cast(DumpFunctionWithDumpObject, func)
        return partial(func, dump_object=dump_object)
    func = cast(DumpFunction, func)
    return func


def build_custom_loader_func(
    func: CustomLoadFunction,
    load_object: LoadFunction
) -> LoadFunction:
    """
    Pass load object function if it required
    """
    sig = signature(func)

    if 'load_object' in sig.parameters:
        func = cast(LoadFunctionWithLoadObject, func)
        return partial(func, load_object=load_object)
    func = cast(LoadFunction, func)
    return func


basic_type_dumpers: BasicTypeDumpers = {
    int: dump_int,
    long: dump_long,
    int128: dump_int128,
    int256: dump_int256,
    float: dump_double,
    bytes: dump_bytes,
    str: dump_string,
}


def load_empty(x: bytes) -> LoadedValue[None]:
    return LoadedValue(None, 0)


basic_type_loaders: BasicTypeLoaders = {
    bytes: load_bytes,
    int: load_int,
    long: load_long,
    int128: load_int128,
    int256: load_int256,
    float: load_double,
    str: load_string,
    type(None): load_empty,
}


def dump_param(
    param: Value2Dump,
    dumpers: CustomDumpersMap,
    dump_object: DumpFunction
) -> bytes:
    origin = param.param.origin
    field = param.param.field

    if is_optional_type(origin):
        origin = origin.__args__[0]

    if is_list_type(origin):
        item_origin = origin.__args__[0]

        if item_origin in basic_type_dumpers:
            dump_item = basic_type_dumpers[item_origin]
        elif item_origin in dumpers:
            func = dumpers[item_origin]
            dump_item = partial(
                build_custom_dumper_func(func, dump_object=dump_object),
                bare=is_bare_item_field(field)
            )
        else:
            dump_item = partial(dump_object, bare=is_bare_item_field(field))

        return dump_vector(
            dump_item,
            param.value,
            is_bare_field(field)
        )

    if origin in basic_type_dumpers:
        return basic_type_dumpers[origin](param.value)

    if origin in dumpers:
        func = build_custom_dumper_func(
            dumpers[origin],
            dump_object=dump_object
        )
    else:
        func = dump_object

    return func(param.value, bare=is_bare_field(field))


def _dump(
    value: Any,
    schema: Schema,
    bare: bool = False,
    custom_dumpers: Optional[CustomDumpersMap] = None
):
    """
    Dumps basic or boxed types by schema
    """
    if custom_dumpers is None:
        custom_dumpers = {}

    data: Optional[Union[CombinatorData, FunctionData]] = None
    values_2_dump: List[Value2Dump] = []

    dumped_values: List[bytes] = []
    flags_value: Optional[int] = None

    if type(value) in custom_dumpers:
        origin = type(value)
        func = build_custom_dumper_func(
            custom_dumpers[origin],
            dump_object=partial(
                _dump,
                schema=schema,
                custom_dumpers=custom_dumpers
            )
        )
        return func(value, bare=bare)

    if isinstance(value, CallableFunc):
        try:
            data = schema[value.func]
        except KeyError:
            raise DumpError('Can`t dump function that not in schema')
        values_2_dump = [
            Value2Dump(value.params.get(param.name), param)
            for param in data.params
        ]
    else:
        try:
            data = schema[type(value)]
        except KeyError:
            raise DumpError('Can`t dump combinator that not in schema')

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

        if 'flag' in getattr(param.field, 'metadata', {}):
            if attr_value is None:
                continue

            type_name = param.type
            flags_value = cast(int, flags_value)
            param_origin = cast(Type, data.origin)
            param_name = param.name

            flags_value = set_flag_value(
                flags_value,
                param_name,
                param_origin
            )
        else:
            type_name = param.type

        try:
            dumped_values.append(
                dump_param(
                    item,
                    dumpers=custom_dumpers,
                    dump_object=partial(
                        _dump,
                        schema=schema,
                        custom_dumpers=custom_dumpers
                    )
                )
            )
        except Exception:
            raise DumpError(f'Can`t dump value {type_name}.')

    dumped_flag = dump_int(flags_value) if flags_value is not None else b''

    constructor = dump_int(data.id) if not bare else b''

    dumped = b''.join(
        [
            constructor,
            dumped_flag
        ] +
        dumped_values
    )
    return dumped


def dump(
    value: Any,
    schema: Schema,
    custom_dumpers: Optional[CustomDumpersMap] = None
):
    return _dump(value, schema=schema, custom_dumpers=custom_dumpers)


def _load(
        input: bytes,
        schema: Schema,
        bare: bool = False,
        tp: Optional[Any] = None,
        custom_loaders: Optional[CustomLoadersMap] = None
) -> LoadedValue[Union[CallableFunc, Any]]:
    """
    Loads object or function with params from bytes input

    Args:
        input - serialized value
        schema - schema that will be used to load
        bare - checks is loaded bytes are bare type or not
        tp - select how type should be loaded
        custom_loaders - custom loaders to load value

    Raises:
        ValueError - when can't load data
    """
    if custom_loaders is None:
        custom_loaders = {}

    if tp in basic_type_loaders:
        basic_loader = basic_type_loaders[tp]
        return basic_loader(input)

    if tp in custom_loaders:
        custom_loader = build_custom_loader_func(
            custom_loaders[tp],
            load_object=partial(
                _load,
                schema=schema,
                custom_loaders=custom_loaders
            )
        )
        return custom_loader(input, bare=bare)

    if tp is None and bare:
        raise ValueError('We should load not bare type or pass combinator')

    offset = 0
    if not bare:
        loaded_combinator = load_int(input)
        offset += loaded_combinator.offset
        combinator = loaded_combinator.value

        if combinator not in schema:
            raise ValueError(f'Can`t find combinator {combinator} in schema')

        data = schema[combinator]
        if data.origin in custom_loaders:
            custom_loader = build_custom_loader_func(
                custom_loaders[data.origin],
                load_object=partial(
                    _load,
                    schema=schema,
                    custom_loaders=custom_loaders
                )
            )
            return custom_loader(input, bare=False)
    else:
        tp = cast(Type, tp)
        if tp not in schema:
            raise ValueError(f'Can`t find info about {tp}')
        data = schema[tp]

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
            item_origin = origin.__args__[0]
            load_item = partial(
                _load,
                bare=is_bare_item_field(param.field),
                schema=schema,
                tp=item_origin,
                custom_loaders=custom_loaders,
            )
            load_func: Callable[[bytes], LoadedValue[Any]] = partial(
                load_vector,
                load_item,
                bare=is_bare_field(param.field)
            )
        else:
            load_func = partial(
                _load,
                bare=is_bare_field(param.field),
                tp=origin,
                schema=schema,
                custom_loaders=custom_loaders,
            )

        loaded = load_func(input[offset:])
        params[param.name] = loaded.value
        offset += loaded.offset

    if isfunction(data.origin):
        value = CallableFunc(data.origin, params)
    else:
        value = data.origin(**params)

    return LoadedValue(value=value, offset=offset)


def load(
    input: bytes,
    schema: Schema,
    custom_loaders: Optional[CustomLoadersMap] = None
) -> LoadedValue[Any]:
    return _load(input, schema=schema, custom_loaders=custom_loaders)
