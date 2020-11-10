# -*- coding: utf-8 -*-
from typing import List, Any, NewType, Optional, ForwardRef, Union
from collections import OrderedDict

from .exceptions import InvalidCombinator


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
        constructors: Optional[List[Any]] = None
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
