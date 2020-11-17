# -*- coding: utf-8 -*-
from typing import NamedTuple, NewType, Union, ForwardRef, List, Optional

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
    is_optional_type,
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


class MessageActionChatAddUser(NamedTuple):
    users: List[int]

    class Meta:
        name = 'messageActionChatAddUser'
        order = ('users', )


MessageAction = NewType('MessageAction', Union[MessageActionChatAddUser])


class ChatParticipantCombinator(NamedTuple):
    user_id: int
    inviter_id: int
    date: int

    class Meta:
        name = 'chatParticipant'
        order = ('user_id', 'inviter_id', 'date')


class ChatParticipantCreator(NamedTuple):
    user_id: int

    class Meta:
        name = 'chatParticipantCreator'
        order = ('user_id', )


class ChatParticipantAdmin(NamedTuple):
    user_id: int
    inviter_id: int
    date: int

    class Meta:
        meta = 'chatParticipantAdmin'


ChatParticipant = NewType(
    'ChatParticipant',
    Union[
        ChatParticipantCombinator,
        ChatParticipantCreator,
        ChatParticipantAdmin
    ]
)


class ChatParticipantsCombinator(NamedTuple):
    chat_id: int
    participants: List[ChatParticipant]
    version: int

    class Meta:
        name = 'chatParticipants'
        order = ('chat_id', 'participants', 'version')


ChatParticipants = NewType('ChatParticipants', ChatParticipantCombinator)


class InputMediaPhotoExternal(NamedTuple):
    url: str
    ttl_seconds: Optional[int]

    class Meta:
        name = 'inputMediaPhotoExternal'
        order = ('url', 'ttl_seconds')
        flags = {
            'ttl_seconds': 0,
        }


InputMedia = NewType('InputMedia', InputMediaPhotoExternal)


class DialogFilterCombinator(NamedTuple):
    class Meta:
        name = 'dialogFilter'


DialogFilter = NewType('DialogFilter', DialogFilterCombinator)


class UpdateDialogFilter(NamedTuple):
    id: int
    filter: Optional[DialogFilter]

    class Meta:
        name = 'updateDialogFilter'
        order = ('id', 'filter')
        flags = {
            'filter': 0
        }


Update = NewType('Update', UpdateDialogFilter)


class ExtendedTreeNode(NamedTuple):
    val: int
    left: Optional['ExtendedTree']
    right: Optional['ExtendedTree']

    class Meta:
        name = 'extendedTreeNode'
        order = ('val', 'left', 'right')
        flags = {
            'left': 0,
            'right': 1,
        }


ExtendedTree = NewType('ExtendedTree', ExtendedTreeNode)


class WithoutFlags(NamedTuple):
    val: Optional[int]

    class Meta:
        name = 'withoutFlags'
        order = ('val', )


class WrongConstructorUsed(NamedTuple):
    val: Optional[AnotherClass]

    class Meta:
        name = 'withoutFlags'
        order = ('val', )
        flags = {
            'val': 0,
        }


class TestIsNamedTuple:

    def test_correct(self):
        assert is_named_tuple(BoolTrue)

    def test_simple_tuple(self):
        assert not is_named_tuple(tuple)

    def test_wrong_type(self):
        assert not is_named_tuple(int)


class TestIsOptionalType:

    def test_base_type(self):
        assert not is_optional_type(int)

    def test_named_tupele(self):
        assert not is_optional_type(ChatParticipantAdmin)

    def test_optional_base_type(self):
        assert is_optional_type(Optional[int])

    def test_optional_constructor_type(self):
        assert is_optional_type(Optional[MessageAction])


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

    def test_list_combinator(self):
        is_valid_combinator(MessageActionChatAddUser)
        is_valid_combinator(ChatParticipantsCombinator, [ChatParticipant])

    def test_valid_optional_base_type_field(self):
        is_valid_combinator(InputMediaPhotoExternal)

    def test_invalid_declared_optional_field(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(WithoutFlags)

    def test_valid_optional_constructor_field(self):
        is_valid_combinator(UpdateDialogFilter, [Update, DialogFilter])
        is_valid_combinator(ExtendedTreeNode, [ExtendedTree])

    def test_invalid_not_constructor_optional_field(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(WrongConstructorUsed)


class TestIsValidConstructor:

    def test_single_combinator(self):
        is_valid_constructor(User)

    def test_union_of_combinators(self):
        is_valid_constructor(Bool, [Bool, Tree])
        is_valid_constructor(Tree, [Bool, Tree])
        is_valid_constructor(ExtendedTree, [ExtendedTree])

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

    def test_list_combinator_message_action(self):
        assert build_combinator_description(
            MessageActionChatAddUser,
            MessageAction
        ) == 'messageActionChatAddUser users:Vector<int> = MessageAction'
        assert build_combinator_description(
            MessageActionChatAddUser,
            MessageAction,
            for_combinator_number=True,
        ) == 'messageActionChatAddUser users:Vector int = MessageAction'

    def test_list_chat_participants(self):
        assert build_combinator_description(
            ChatParticipantsCombinator,
            ChatParticipants,
        ) == 'chatParticipants chat_id:int participants:Vector<ChatParticipant> version:int = ChatParticipants'  # noqa
        assert build_combinator_description(
            ChatParticipantsCombinator,
            ChatParticipants,
            for_combinator_number=True
        ) == 'chatParticipants chat_id:int participants:Vector ChatParticipant version:int = ChatParticipants'  # noqa

    def test_optional_basic_type(self):
        assert build_combinator_description(
            InputMediaPhotoExternal,
            InputMedia
        ) == 'inputMediaPhotoExternal flags:# url:string ttl_seconds:flags.0?int = InputMedia'  # noqa

    def test_optional_constructor_type(self):
        assert build_combinator_description(
            UpdateDialogFilter,
            Update
        ) == 'updateDialogFilter flags:# id:int filter:flags.0?DialogFilter = Update'  # noqa

    def test_several_optional_constructor_type(self):
        assert build_combinator_description(
            ExtendedTreeNode,
            ExtendedTree
        ) == 'extendedTreeNode flags:# val:int left:flags.0?ExtendedTree right:flags.1?ExtendedTree = ExtendedTree'  # noqa


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

    def test_message_action(self):
        assert get_combinator_number(
            MessageActionChatAddUser,
            MessageAction
        ) == 0x488a7337

    def test_chart_participants(self):
        assert get_combinator_number(
            ChatParticipantsCombinator,
            ChatParticipants
        ) == 0x3f460fed

    def test_input_media(self):
        assert get_combinator_number(
            InputMediaPhotoExternal,
            InputMedia
        ) == 0xe5bbfe1a

    def test_update(self):
        assert get_combinator_number(
            UpdateDialogFilter,
            Update
        ) == 0x26ffde7d
