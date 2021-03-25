# -*- coding: utf-8 -*-
import binascii
from typing import (
    List,
    Any,
    Type,
    NewType,
    Optional,
    ForwardRef,
    NamedTuple,
    Union,
    Annotated,
    Callable,
    get_origin,
    get_args,
)
from dataclasses import is_dataclass, fields
from inspect import signature, iscoroutinefunction, Parameter
from math import log

from .exceptions import (
    InvalidCombinator,
    InvalidConstructor,
    InvalidFunction,
)


PossibleConstructors = Optional[List[Any]]


long = NewType('long', int)
int128 = NewType('int128', int)
int256 = NewType('int256', int)
double = NewType('double', float)


BASIC_TYPES = [str, bytes, int, long, int128, int256, double, Any]


def is_union(tp: Any) -> bool:
    return get_origin(tp) == Union


def is_annotated(tp: Any) -> bool:
    return get_origin(tp) == Annotated


def get_constructor_name(c: Any) -> str:
    if isinstance(c, str):
        return c

    if is_dataclass(c):
        return c.__name__

    if is_annotated(c):
        return c.__metadata__[0]

    return getattr(c, '_name', '')


def is_list_type(tp: Any) -> bool:
    return getattr(tp, '__origin__', None) == list


def is_optional_type(tp: Any) -> bool:
    return (
        hasattr(tp, '__args__') and
        len(tp.__args__) >= 2 and
        tp.__args__[-1] is type(None)  # noqa: E721
    )


def is_annotated_union(tp) -> bool:
    return is_annotated(tp) and is_union(tp.__args__[0])


def get_combinators(tp) -> List[Any]:
    """
    Assume that constructor is annotated union.
    Returns list of types
    """
    return [
        combinator
        for combinator in tp.__args__[0].__args__
    ]


def is_allowed_type(
    value: Any,
    constructors: PossibleConstructors = None
) -> bool:
    """
    Check simple types of ForwardRef to used for combinator
    """
    if constructors is None:
        constructors = []

    constructor_names = [get_constructor_name(c) for c in constructors]

    if isinstance(value, str):
        return value in constructor_names

    if isinstance(value, ForwardRef):
        type_name = value.__forward_arg__

        return type_name in constructor_names

    available_types = BASIC_TYPES + constructors

    return value in available_types


def is_good_for_combinator(
    value: Any,
    constructors: PossibleConstructors = None
) -> bool:
    """
    Checks is passed type could be used for combinator.
    Types that accept for combinators are basic types, constructors,
    optional basic types, constructors, list of basic types, constructors

    Args:
        value: type to check
        constructors: availables constructors

    Returns:
        is passed type good for combinator or not
    """
    check_type = value
    if is_optional_type(check_type):
        check_type = check_type.__args__[0]

    if is_list_type(check_type):
        check_type = check_type.__args__[0]

    return is_allowed_type(check_type, constructors=constructors)


def is_valid_combinator(
    combinator: Any,
    constructors: Optional[List[Any]] = None
) -> None:
    """
    Checks is passed value correct combinator or not. Combinator is NamedTuple
    with Meta class. Named tuple attribute types could be one of bare types:
    `str`, 'bytes', `int`, 'long', 'int128', 'int256', 'double' or other
    combinator/constructor. All attributes in combinator should be described
    in order attribute of

    Args:
        combinator: type to check is it combinator or not
        constructors: List of constructors that could be used to build
                      combinator

    Raises:
        InvalidCombinator - when incorrect combinator has been passed

    """
    c_name = combinator.__name__

    if not is_dataclass(combinator):
        raise InvalidCombinator(
            f'Combinator {c_name} should be subclass of NamedTuple'
        )

    if not hasattr(combinator, 'Meta'):
        raise InvalidCombinator(
            f'Combinator {c_name} should have Meta attribute'
        )

    if (
        not hasattr(combinator.Meta, 'name') or
        not isinstance(combinator.Meta.name, str) or
        not combinator.Meta.name
    ):
        raise InvalidCombinator(
            f'Combinator {c_name} should have name attribute in Meta '
        )

    order = getattr(combinator.Meta, 'order', [])
    flags = getattr(combinator.Meta, 'flags', [])

    for attr_name in order:
        if attr_name not in combinator.__dataclass_fields__:
            raise InvalidCombinator(
                f"Missed attribute {attr_name} for combinator {c_name}"
            )

    for field in fields(combinator):
        attr_name = field.name
        attr_type = field.type

        if attr_name not in order:
            raise InvalidCombinator(
                f"Attribute {attr_name} doesn`t set in {c_name} order"
            )

        if not is_good_for_combinator(attr_type, constructors):
            error_str = (
                f'{attr_name} type should be basic or constructor' +
                ' list or optional'
            )
            raise InvalidCombinator(error_str)

        if is_optional_type(attr_type) and attr_name not in flags:
            raise InvalidCombinator(
                f'Attribute {attr_name} should be set in Meta.flags'
            )


def is_valid_constructor(
    value: Any,
    constructors: PossibleConstructors = None
) -> None:
    """
    Check is value is a valid constructor.
    Valid constructor is a constructor that has been created as Union
    with attribute `_name` or single combinator

    Args:
        value: value to check is it constructor or not
        constructors: constructors that could be used
    Raises:
        InvalidCombinator - if combinator is not valid
        InvalidConstructor - if constructor not Annotated Union
    """

    if is_dataclass(value):
        is_valid_combinator(value, constructors)
        return

    if is_union(value):
        for combinator in get_args(value):
            is_valid_combinator(combinator, constructors)
        return

    if is_annotated(value):
        union = get_args(value)[0]
        for combinator in get_args(union):
            is_valid_combinator(combinator, constructors)
        return

    error = 'Constructor should be single combinator or union of combinators'
    raise InvalidConstructor(error)


def is_string_type_name(type_name: str, for_type_number) -> bool:
    return type_name == 'str' or (type_name == 'bytes' and for_type_number)


def get_type_name(
    attr_type: Any,
    attr_name: Optional[str] = None,
    combinator: Optional[Any] = None,
    for_type_number: bool = False
) -> str:
    """
    Returns mtproto type of attribute
    Args:
        attr_type: basic type, forward ref of constructor
        attr_name: name to get order for optional type
        combinator: base combinator to detect order for optional field
        for_type_number: dump description for combinator number
    """
    if attr_type in BASIC_TYPES:
        if attr_type == Any:
            return 'Object'
        type_name = attr_type.__name__
        if is_string_type_name(type_name, for_type_number):
            return 'string'
        return type_name

    if isinstance(attr_type, ForwardRef):
        return attr_type.__forward_arg__

    if is_list_type(attr_type):
        list_item_type = get_type_name(attr_type.__args__[0],
                                       for_type_number=for_type_number)
        if for_type_number:
            return f'Vector {list_item_type}'
        return f'Vector<{list_item_type}>'

    if is_optional_type(attr_type) and combinator is not None:
        optional_type_name = get_type_name(attr_type.__args__[0],
                                           for_type_number=for_type_number)
        order = combinator.Meta.flags[attr_name]

        return f'flags.{order}?{optional_type_name}'

    return get_constructor_name(attr_type)


class AttrDescription(NamedTuple):
    """
    Describes attribute or function parameter with name and type of it
    """
    name: str  # name of parameter
    type: str  # name of type
    origin: Type  # origin type


def build_attr_description(
    attr_name: str,
    attr_type: Any,
    combinator: Any,
    for_type_number: bool = False
) -> AttrDescription:
    """
    Description string contains attribute name and attribute type name

    Args:
        attr_name: name of attribute
        attr_type: type of attribute
        combinator: combinator for whom we build description
        for_type_number: dump description for combinator number
    """
    attr_type_str = get_type_name(attr_type, attr_name=attr_name,
                                  combinator=combinator,
                                  for_type_number=for_type_number)

    return AttrDescription(attr_name, attr_type_str, attr_type)


def build_attr_description_list(
    combinator: Any,
    for_type_number: bool = False
) -> List[AttrDescription]:
    """
    Builds list of description attributes of combinator in meta order

    Args:
        combinator: combinator wich attrs should be described
        for_type_number: dump description for combinator number
    Returns:
        list of described attributes
    """
    order = getattr(combinator.Meta, 'order', [])
    flags_attr_list = []

    if hasattr(combinator.Meta, 'flags'):
        flags_attr_list.append(AttrDescription('flags', '#', int))

    return flags_attr_list + [
        build_attr_description(
            attr_name,
            combinator.__dataclass_fields__[attr_name].type,
            combinator=combinator,
            for_type_number=for_type_number
        )
        for attr_name in order
    ]


def build_combinator_description(
    combinator: Any,
    constructor: Any,
    for_type_number: bool = False
) -> str:
    """
    Assume that only correct combinator passed to this function
    Parses combinator type to build description string. See
    https://core.telegram.org/mtproto/serialize

    Args:
        combinator: combinator to build description
        constructor: result constructor of this combinator
        for_type_number: dump description for combinator number

    Returns:
        string expression
    """
    description_strings = [
        f'{description.name}:{description.type}'
        for description in
        build_attr_description_list(
            combinator,
            for_type_number=for_type_number
        )
    ]
    return " ".join(
        [combinator.Meta.name] +
        description_strings +
        ["=", get_constructor_name(constructor)]
    )


def get_combinator_number(combinator: Any, constructor: Any) -> int:
    """
    Type number or type name is a 32-bit number that uniquely identifies a type
    it normally is the sum of the CRC32 values of the descriptions
    of the type constructors. See https://core.telegram.org/mtproto/serialize

    Args:
        combinator: - combinator that should be computed
        constructor: - constructor of computed combinator

    Returns:
        crc32 number for combinator
    """
    description = build_combinator_description(
        combinator,
        constructor,
        for_type_number=True
    )
    description_bytes = description.encode()

    return binascii.crc32(description_bytes)


def is_valid_function(
    func: Callable,
    constructors: PossibleConstructors = None
) -> None:
    """
    Checks is passed func valid and could be used in schema.
    Valid function is async function that accepts only basic types and
    constructor as parameters and return values

    Args:
        func: function that should be schecked
        constructors: available constructors

    Raises:
        InvalidFunction
    """
    if constructors is None:
        constructors = []

    if not iscoroutinefunction(func):
        raise InvalidFunction("Functions should be async")

    sig = signature(func)

    for parameter in sig.parameters.values():
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise InvalidFunction(
                "Function accepts only default python parameters" +
                "(POSITIONAL_OR_KEYWORD)"
            )
        check_type = parameter.annotation

        if is_list_type(check_type):
            check_type = check_type.__args__[0]

        if not is_allowed_type(check_type, constructors):
            raise InvalidFunction(
                f"Parameter {parameter.name} should be basic type " +
                "or one of constructors or vector of allowed types"
            )

    if not is_allowed_type(sig.return_annotation, constructors):
        raise InvalidFunction(
            "Return value should be basic type or one of constructors"
        )


def get_function_name(func: Callable) -> str:
    return func.__name__


def get_funciton_parameters_list(
        func: Callable,
        for_type_number: bool = False,
) -> List[AttrDescription]:
    """
    Parses function parameters and return it as list

    Args:
        func - function which params should be returns
        for_type_number: will we use for computing combinator number
    """
    sig = signature(func)
    return [
        AttrDescription(
            name=p.name,
            type=get_type_name(p.annotation, for_type_number=for_type_number),
            origin=p.annotation
        )
        for p in sig.parameters.values()
    ]


def get_function_return_type_name(func) -> str:
    """
    returns name of function return annotation type

    Args:
        func: function that should be described
    """
    sig = signature(func)
    return get_type_name(sig.return_annotation)


def build_function_description(
    func: Callable,
    for_type_number: bool = False
) -> str:
    """
    Assume we've got valid functions. We could build a valid description string

    Args:
        func: function that should be described
        for_type_number: will we use for computing combinator number

    Returns:
        function description string
    """
    parameter_list = get_funciton_parameters_list(
        func,
        for_type_number=for_type_number
    )
    return " ".join(
        [
            get_function_name(func)
        ] +
        [
            f'{p.name}:{p.type}'
            for p in parameter_list
        ] +
        [
            "=",
            get_function_return_type_name(func)
        ]
    )


def get_function_number(func: Callable) -> int:
    """
    Type number for function computes as crc32 from
    function description string. Assume that func is a valid function

    Args:
        func: function for computing number

    Returns:
        function number
    """
    description = build_function_description(func, for_type_number=True)
    return binascii.crc32(description.encode())


def bytes_needed(n: int) -> int:
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


def dump_integer_big_endian(value: int) -> bytes:
    """
    Dumps integer with minimum number of bytes in big endian order
    """
    return value.to_bytes(
        bytes_needed(value),
        'big'
    )
