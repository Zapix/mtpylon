# -*- coding: utf-8 -*-
from typing import NamedTuple

import pytest

from mtpylon.exceptions import InvalidCombinator
from mtpylon.utils import is_named_tuple, is_valid_combinator


class BoolTrue(NamedTuple):
    class Meta:
        name = 'boolTrue'


class BoolFalse(NamedTuple):
    class Meta:
        name = 'boolFalse'


class IncorrectNoMetaCombinator(NamedTuple):
    pass


class IncorrectNoNameCombinator(NamedTuple):
    class Meta:
        pass


class IncorrectEmptyNameCombinator(NamedTuple):
    class Meta:
        name = ''


class IncorrectNameCombinator(NamedTuple):
    class Meta:
        name = 323


class TestIsNamedTuple:

    def test_correct(self):
        assert is_named_tuple(BoolTrue)

    def test_simple_tuple(self):
        assert not is_named_tuple(tuple)

    def test_wrong_type(self):
        assert not is_named_tuple(int)


class TestIsValidCombinator:

    def test_empty_correct_combinator(self):
        is_valid_combinator(BoolTrue)
        is_valid_combinator(BoolFalse)

    def test_no_meta_in_combinator(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(IncorrectNoMetaCombinator)

    def test_no_name_in_combinator(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(IncorrectNoNameCombinator)

    def test_wrong_name_in_combinator(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(IncorrectEmptyNameCombinator)

        with pytest.raises(InvalidCombinator):
            is_valid_combinator(IncorrectNameCombinator)
