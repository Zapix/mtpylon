# -*- coding: utf-8 -*-
from typing import NamedTuple, NewType, Union, ForwardRef

import pytest

from mtpylon.exceptions import InvalidCombinator, InvalidConstructor
from mtpylon.utils import (
    is_named_tuple,
    is_valid_combinator,
    is_valid_constructor,
    is_good_for_combinator
)


class BoolTrue(NamedTuple):
    class Meta:
        name = 'boolTrue'


class BoolFalse(NamedTuple):
    class Meta:
        name = 'boolFalse'


Bool = NewType('Bool', Union[BoolTrue, BoolFalse])


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


IncorrectConstructor = NewType(
    'IncorrectConstructor', IncorrectNoMetaCombinator)


class UserCombinator(NamedTuple):
    id: int
    name: str

    class Meta:
        name = 'user'
        order = ('id', 'name')


User = NewType('User', UserCombinator)


class NotInOrder(NamedTuple):
    id: int
    value: int

    class Meta:
        name = 'notInOrder'
        order = ('id',)


class MissedAttribute(NamedTuple):
    id = int

    class Meta:
        name = 'attributedDidNotDescribed'
        order = ('id', 'value')


class TreeNode(NamedTuple):
    value: int
    left_node: 'Tree'
    right_node: 'Tree'

    class Meta:
        name = 'treeNode'
        order = ('value', 'left_node', 'right_node')


class LeafNode(NamedTuple):
    value: int

    class Meta:
        name = 'leafNode'
        order = ('value', )


Tree = NewType('Tree', Union[TreeNode, LeafNode])


class AnotherClass:
    pass


class WrongAttrType(NamedTuple):
    id: int
    value: AnotherClass

    class Meta:
        name = 'wrongAttrType'
        order = ('id', 'value')


class TestIsNamedTuple:

    def test_correct(self):
        assert is_named_tuple(BoolTrue)

    def test_simple_tuple(self):
        assert not is_named_tuple(tuple)

    def test_wrong_type(self):
        assert not is_named_tuple(int)


class TestIsGoodForCombinator:

    def test_basic_type(self):
        assert is_good_for_combinator(str)

    def test_constructor_type(self):
        assert is_good_for_combinator(Bool, [Bool, Tree])

    def test_constructor_forward_ref(self):
        assert is_good_for_combinator(ForwardRef('Tree'), [Bool, Tree])

    def test_constructor_annotation(self):
        left_node_type = TreeNode.__annotations__['left_node']
        assert is_good_for_combinator(left_node_type, [Bool, Tree])

    def test_wrong_value(self):
        assert not is_good_for_combinator(AnotherClass)

    def test_wrong_forward_ref(self):
        assert not is_good_for_combinator(ForwardRef('Tree'), [Bool])


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

    def test_combinator_with_attributes(self):
        is_valid_combinator(UserCombinator)

    def test_attribute_is_not_in_order(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(NotInOrder)

    def test_missed_attribute(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(MissedAttribute)

    def test_wrong_attribute(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(WrongAttrType)

    def test_recursive_combinator(self):
        is_valid_combinator(TreeNode, [Bool, Tree])


class TestIsValidConstructor:

    def test_single_combinator(self):
        is_valid_constructor(User)

    def test_union_of_combinators(self):
        is_valid_constructor(Bool, [Bool, Tree])
        is_valid_constructor(Tree, [Bool, Tree])

    def test_wrong_value(self):
        with pytest.raises(InvalidConstructor):
            is_valid_constructor(int)
