# -*- coding: utf-8 -*-
from typing import Any
from collections import OrderedDict

from .exceptions import InvalidCombinator


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


def is_valid_combinator(combinator: Any) -> None:
    """
    Checks is passed value correct combinator or not. Combinator is NamedTuple
    with Meta class. Named tuple attribute types could be one of bare types:
    `str`, 'bytes', `int`, 'long', 'int128', 'int256', 'double' or other
    combinator/constructor

    Args:
        combinator: type to check is it combinator or not

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
