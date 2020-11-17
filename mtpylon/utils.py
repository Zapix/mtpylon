# -*- coding: utf-8 -*-
import binascii
from typing import (
    List,
    Any,
    NewType,
    Optional,
    ForwardRef,
)
from collections import OrderedDict

from .exceptions import InvalidCombinator, InvalidConstructor

PossibleConstructors = Optional[List[Any]]

long = NewType('long', int)
int128 = NewType('int128', int)
int256 = NewType('int256', int)
double = NewType('double', float)

BASIC_TYPES = [str, bytes, int, long, int128, int256, double]


def is_named_tuple(value: type) -> bool:
    """
    Checks is passed type is named tuple or not

    Args:
        value - class to check

    Returns:
        true if class is named tuple
    """

    return (
        issubclass(value, tuple) and
        hasattr(value, '__annotations__') and
        isinstance(value.__annotations__, (dict, OrderedDict))
    )


def is_list_type(tp: Any) -> bool:
    return getattr(tp, '__origin__', None) == list


def is_optional_type(tp: Any) -> bool:
    return (
        hasattr(tp, '__args__') and
        len(tp.__args__) == 2 and
        tp.__args__[1] is type(None)  # noqa: E721
    )


def is_allowed_type(
        value: Any,
        constructors: PossibleConstructors = None
) -> bool:
    """
    Check simple types of ForwardRef to used for combinator
    :param value:
    :param constructors:
    :return:
    """
    if constructors is None:
        constructors = []

    if isinstance(value, ForwardRef):
        type_name = value.__forward_arg__
        constructor_names = [c.__name__ for c in constructors]

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

    if not is_named_tuple(combinator):
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
        if attr_name not in combinator.__annotations__:
            raise InvalidCombinator(
                f"Missed attribute {attr_name} for combinator {c_name}"
            )

    for (attr_name, attr_type) in combinator.__annotations__.items():
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
    Valid constructor is a constructor that has been created by NewType
    and could be combinator or union of combinators

    Args:
        value: value to check is it constructor or not
        constructors: constructors that could be used
    Raises:
        InvalidCombinator - if combinator is not valid
        InvalidConstructor - if constructor not NewType
    """
    error = 'Constructor should be NewType combinator or union of combinators'

    if not hasattr(value, '__supertype__'):
        raise InvalidConstructor(error)

    supertype = value.__supertype__
    if hasattr(supertype, '__args__'):  # assume it's union of combinators
        combinators = supertype.__args__

        for combinator in combinators:
            is_valid_combinator(combinator, constructors)
    else:
        is_valid_combinator(supertype, constructors)


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

    return attr_type.__name__


def _build_attr_description(
        attr_name: str,
        attr_type: Any,
        combinator: Any,
        for_combinator_number: Optional[bool] = False
) -> str:
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

    return f'{attr_name}:{attr_type_str}'


def _build_attr_description_list(
        combinator: Any,
        for_combinator_number: Optional[bool] = False
) -> List[str]:
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
        flags_attr_list.append('flags:#')

    return flags_attr_list + [
        _build_attr_description(
            attr_name,
            combinator.__annotations__[attr_name],
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
    return " ".join(
        [combinator.Meta.name] +
        _build_attr_description_list(
            combinator,
            for_combinator_number=for_combinator_number
        ) +
        ["=", constructor.__name__]
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
