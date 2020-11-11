# -*- coding: utf-8 -*-
import binascii
from typing import (
    List,
    Any,
    NewType,
    Optional,
    ForwardRef,
    Union,
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


def is_good_for_combinator(
        value: Union[type, ForwardRef],
        constructors: PossibleConstructors = None
) -> bool:
    """
    Checks is passed type could be used for combinator.
    Types that accept for combinators ar basic types or constructors

    Args:
        value: type to check
        constructors: availables constructors

    Returns:
        is passed type good for combinator or not
    """
    if constructors is None:
        constructors = []

    if value in BASIC_TYPES:
        return True

    if value in constructors:
        return True

    if isinstance(value, ForwardRef):
        type_name = value.__forward_arg__
        constructor_names = [c.__name__ for c in constructors]

        return type_name in constructor_names

    return False


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
            raise InvalidCombinator(
                f'Attribute type of {attr_name} should be basic or constructor'
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


def _get_type_name(attr_type: Any) -> str:
    """
    Returns mtproto type of attribute
    Args:
        attr_type: basic type, forward ref of constructor
    """
    if attr_type in BASIC_TYPES:
        type_name = attr_type.__name__
        return 'string' if type_name == 'str' else type_name

    if isinstance(attr_type, ForwardRef):
        return attr_type.__forward_arg__

    return attr_type.__name__


def _build_attr_description(attr_name: str, attr_type: Any) -> str:
    """
    Description string contains attribute name and attribute type name

    Args:
        attr_name: name of attribute
        attr_type: type of attribute
    """
    attr_type_str = _get_type_name(attr_type)

    return f'{attr_name}:{attr_type_str}'


def _build_attr_description_list(combinator: Any) -> List[str]:
    """
    Builds list of description attributes of combinator in meta order

    Args:
        combinator: combinator wich attrs should be described
    Returns:
        list of described attributes
    """
    order = getattr(combinator.Meta, 'order', [])
    return [
        _build_attr_description(
            attr_name,
            combinator.__annotations__[attr_name]
        )
        for attr_name in order
    ]


def build_combinator_description(combinator: Any, constructor: Any) -> str:
    """
    Assume that only correct combinator passed to this function
    Parses combinator type to build description string. See
    https://core.telegram.org/mtproto/serialize

    Args:
        combinator: combinator to build description
        constructor: result constructor of this combinator

    Returns:
        string expression
    """
    return " ".join(
        [combinator.Meta.name] +
        _build_attr_description_list(combinator) +
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
    description = build_combinator_description(combinator, constructor)
    description_bytes = description.encode()

    return binascii.crc32(description_bytes)
