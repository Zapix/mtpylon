# -*- coding: utf-8 -*-
from typing import NamedTuple, NewType, Union, ForwardRef

import pytest

from mtpylon.exceptions import InvalidCombinator, InvalidConstructor
from mtpylon.utils import (
    long,
    is_named_tuple,
    is_valid_combinator,
    is_valid_constructor,
    is_good_for_combinator,
    build_combinator_description,
    get_combinator_number,
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


class InputPeerEmpty(NamedTuple):
    class Meta:
        name = 'inputPeerEmpty'


class InputPeerSelf(NamedTuple):
    class Meta:
        name = 'inputPeerSelf'


class InputPeerChat(NamedTuple):
    chat_id: int

    class Meta:
        name = 'inputPeerChat'
        order = ('chat_id', )


class InputPeerUser(NamedTuple):
    user_id: int
    access_hash: long

    class Meta:
        name = 'inputPeerUser'
        order = ('user_id', 'access_hash', )


class InputPeerChannel(NamedTuple):
    channel_id: int
    access_hash: long

    class Meta:
        name = 'inputPeerChannel'
        order = ('channel_id', 'access_hash', )


class InputPeerUserFromMessage(NamedTuple):
    peer: 'InputPeer'
    msg_id: int
    user_id: int

    class Meta:
        name = 'inputPeerUserFromMessage'
        order = ('peer', 'msg_id', 'user_id', )


class InputPeerChannelFromMessage(NamedTuple):
    peer: 'InputPeer'
    msg_id: int
    channel_id: int

    class Meta:
        name = 'inputPeerChannelFromMessage'
        order = ('peer', 'msg_id', 'channel_id', )


InputPeer = NewType(
    'InputPeer',
    Union[
        InputPeerEmpty,
        InputPeerSelf,
        InputPeerChat,
        InputPeerUser,
        InputPeerChannel,
        InputPeerUserFromMessage,
        InputPeerChannelFromMessage
    ]
)


class TaskCombinator(NamedTuple):
    content: str
    finished: Bool

    class Meta:
        name = 'task'
        order = ('content', 'finished')


Task = NewType('Task', TaskCombinator)


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


class TestBuildCombinatorDescription:

    def test_empty_combinator(self):
        assert build_combinator_description(BoolTrue, Bool) == (
            'boolTrue = Bool'
        )
        assert build_combinator_description(BoolFalse, Bool) == (
            'boolFalse = Bool'
        )

    def test_simple_combinator(self):
        assert build_combinator_description(LeafNode, Tree) == (
            'leafNode value:int = Tree'
        )
        assert build_combinator_description(UserCombinator, User) == (
            'user id:int name:string = User'
        )

    def test_recursive_combinator(self):
        assert build_combinator_description(TaskCombinator, Task) == (
            'task content:string finished:Bool = Task'
        )
        assert build_combinator_description(TreeNode, Tree) == (
            'treeNode value:int left_node:Tree right_node:Tree = Tree'
        )


class TestCombinatorNumber:

    def test_bool(self):
        assert get_combinator_number(BoolTrue, Bool) == 0x997275b5
        assert get_combinator_number(BoolFalse, Bool) == 0xbc799737

    def test_input_peer(self):
        assertion_list = [
            (InputPeerEmpty, 0x7f3b18ea),
            (InputPeerSelf, 0x7da07ec9),
            (InputPeerChat, 0x179be863),
            (InputPeerUser, 0x7b8e7de6),
            (InputPeerChannel, 0x20adaef8),
            (InputPeerUserFromMessage, 0x17bae2e6),
            (InputPeerChannelFromMessage, 0x9c95f7bb),
        ]

        for combinator, value in assertion_list:
            assert get_combinator_number(combinator, InputPeer) == value
