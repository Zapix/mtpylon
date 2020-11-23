# -*- coding: utf-8 -*-
import binascii
from typing import (
    List,
    Any,
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


BASIC_TYPES = [str, bytes, int, long, int128, int256, double]


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
    if is_list_type(value):
        return is_allowed_type(value.__args__[0], constructors=constructors)

    if is_optional_type(value):
        return is_allowed_type(value.__args__[0], constructors=constructors)

    return is_allowed_type(value, constructors=constructors)


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


def get_type_name(
        attr_type: Any,
        attr_name: Optional[str] = None,
        combinator: Optional[Any] = None,
        for_combinator_number: Optional[bool] = False,
) -> str:
    """
    Returns mtproto type of attribute
    Args:
        attr_type: basic type, forward ref of constructor
        attr_name: name to get order for optional type
        combinator: base combinator to detect order for optional field
        for_combinator_number: dump description for combinator number
    """
    if attr_type in BASIC_TYPES:
        type_name = attr_type.__name__
        return 'string' if type_name == 'str' else type_name

    if isinstance(attr_type, ForwardRef):
        return attr_type.__forward_arg__

    if is_list_type(attr_type):
        list_item_type = get_type_name(
            attr_type.__args__[0],
            for_combinator_number=for_combinator_number
        )
        if for_combinator_number:
            return f'Vector {list_item_type}'
        return f'Vector<{list_item_type}>'

    if is_optional_type(attr_type) and combinator is not None:
        optional_type_name = get_type_name(
            attr_type.__args__[0],
            for_combinator_number=for_combinator_number
        )
        order = combinator.Meta.flags[attr_name]

        return f'flags.{order}?{optional_type_name}'

    return get_constructor_name(attr_type)


class AttrDescription(NamedTuple):
    name: str
    type: str


def build_attr_description(
        attr_name: str,
        attr_type: Any,
        combinator: Any,
        for_combinator_number: Optional[bool] = False
) -> AttrDescription:
    """
    Description string contains attribute name and attribute type name

    Args:
        attr_name: name of attribute
        attr_type: type of attribute
        combinator: combinator for whom we build description
        for_combinator_number: dump description for combinator number
    """
    attr_type_str = get_type_name(
        attr_type,
        attr_name=attr_name,
        combinator=combinator,
        for_combinator_number=for_combinator_number
    )

    return AttrDescription(attr_name, attr_type_str)


def build_attr_description_list(
        combinator: Any,
        for_combinator_number: Optional[bool] = False
) -> List[AttrDescription]:
    """
    Builds list of description attributes of combinator in meta order

    Args:
        combinator: combinator wich attrs should be described
        for_combinator_number: dump description for combinator number
    Returns:
        list of described attributes
    """
    order = getattr(combinator.Meta, 'order', [])
    flags_attr_list = []

    if hasattr(combinator.Meta, 'flags'):
        flags_attr_list.append(AttrDescription('flags', '#'))

    return flags_attr_list + [
        build_attr_description(
            attr_name,
            combinator.__dataclass_fields__[attr_name].type,
            combinator=combinator,
            for_combinator_number=for_combinator_number,
        )
        for attr_name in order
    ]


def build_combinator_description(
        combinator: Any,
        constructor: Any,
        for_combinator_number: Optional[bool] = False
) -> str:
    """
    Assume that only correct combinator passed to this function
    Parses combinator type to build description string. See
    https://core.telegram.org/mtproto/serialize

    Args:
        combinator: combinator to build description
        constructor: result constructor of this combinator
        for_combinator_number: dump description for combinator number

    Returns:
        string expression
    """
    description_strings = [
        f'{description.name}:{description.type}'
        for description in build_attr_description_list(
            combinator,
            for_combinator_number=for_combinator_number
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
        for_combinator_number=True
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


def build_function_description(
        func: Callable,
        for_combinator_number: bool = False
) -> str:
    """
    Assume we've got valid functions. We could build a valid description string

    Args:
        func: function that should be described
        for_combinator_number: will we use for computing combinator number

    Returns:
        function description string
    """
    sig = signature(func)
    parameter_list = [
        AttrDescription(
            name=p.name,
            type=get_type_name(
                p.annotation,
                for_combinator_number=for_combinator_number
            )

        )
        for p in sig.parameters.values()
    ]
    return " ".join(
        [
            func.__name__
        ] +
        [
            f'{p.name}:{p.type}'
            for p in parameter_list
        ] +
        [
            "=",
            get_type_name(sig.return_annotation)
        ]
    )
