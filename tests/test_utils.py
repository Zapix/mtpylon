# -*- coding: utf-8 -*-
from aiohttp.web import Request

from typing import Union, ForwardRef, List, Optional, Annotated, Any
from dataclasses import dataclass, field

import pytest

from mtpylon.exceptions import (
    InvalidCombinator,
    InvalidConstructor,
    InvalidFunction,
)
from mtpylon.utils import (
    is_valid_combinator,
    is_valid_constructor,
    is_valid_function,
    is_good_for_combinator,
    build_combinator_description,
    get_combinator_number,
    is_optional_type,
    build_function_description,
    get_function_number,
    get_fields_map,
)
from mtpylon import long, int128


@dataclass
class BoolTrue:
    class Meta:
        name = 'boolTrue'


@dataclass
class BoolFalse:
    class Meta:
        name = 'boolFalse'


Bool = Annotated[
    Union[BoolTrue, BoolFalse],
    'Bool'
]


@dataclass
class IncorrectNoNameCombinator:
    class Meta:
        pass


@dataclass
class IncorrectEmptyNameCombinator:
    class Meta:
        name = ''


@dataclass
class IncorrectNameCombinator:
    class Meta:
        name = 323


@dataclass
class User:
    id: int
    name: str

    class Meta:
        name = 'user'
        order = ('id', 'name')


@dataclass
class NotInOrder:
    id: int
    value: int

    class Meta:
        name = 'notInOrder'
        order = ('id',)


@dataclass
class MissedAttribute:
    id = int

    class Meta:
        name = 'attributedDidNotDescribed'
        order = ('id', 'value')


@dataclass
class TreeNode:
    value: int
    left_node: 'Tree'
    right_node: 'Tree'

    class Meta:
        name = 'treeNode'
        order = ('value', 'left_node', 'right_node')


@dataclass
class LeafNode:
    value: int

    class Meta:
        name = 'leafNode'
        order = ('value', )


Tree = Annotated[
    Union[TreeNode, LeafNode],
    'Tree'
]


@dataclass
class InputPeerEmpty:
    class Meta:
        name = 'inputPeerEmpty'


@dataclass
class InputPeerSelf:
    class Meta:
        name = 'inputPeerSelf'


@dataclass
class InputPeerChat:
    chat_id: int

    class Meta:
        name = 'inputPeerChat'
        order = ('chat_id', )


@dataclass
class InputPeerUser:
    user_id: int
    access_hash: long

    class Meta:
        name = 'inputPeerUser'
        order = ('user_id', 'access_hash', )


@dataclass
class InputPeerChannel:
    channel_id: int
    access_hash: long

    class Meta:
        name = 'inputPeerChannel'
        order = ('channel_id', 'access_hash', )


@dataclass
class InputPeerUserFromMessage:
    peer: 'InputPeer'
    msg_id: int
    user_id: int

    class Meta:
        name = 'inputPeerUserFromMessage'
        order = ('peer', 'msg_id', 'user_id', )


@dataclass
class InputPeerChannelFromMessage:
    peer: 'InputPeer'
    msg_id: int
    channel_id: int

    class Meta:
        name = 'inputPeerChannelFromMessage'
        order = ('peer', 'msg_id', 'channel_id', )


InputPeer = Annotated[
    Union[
        InputPeerEmpty,
        InputPeerSelf,
        InputPeerChat,
        InputPeerUser,
        InputPeerChannel,
        InputPeerUserFromMessage,
        InputPeerChannelFromMessage
    ],
    'InputPeer'
]


@dataclass
class Task:
    content: str
    finished: Bool

    class Meta:
        name = 'task'
        order = ('content', 'finished')


@dataclass
class TaggedTask:
    content: str
    finished: Bool
    tags: Optional[List[str]] = field(metadata={'flag': 1})

    class Meta:
        name = 'taggedTask'
        order = ('content', 'finished', 'tags')


@dataclass
class ResPQ:
    nonce: int128
    server_nonce: int128
    pq: bytes
    server_public_key_fingerprints: List[long]

    class Meta:
        name = 'resPQ'
        order = (
            'nonce',
            'server_nonce',
            'pq',
            'server_public_key_fingerprints'
        )


@dataclass
class RpcResult:
    req_msg_id: long
    result: Any

    class Meta:
        name = 'rpc_result'
        order = ('req_msg_id', 'result')


class AnotherClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b


@dataclass
class WrongAttrType:
    id: int
    value: AnotherClass

    class Meta:
        name = 'wrongAttrType'
        order = ('id', 'value')


@dataclass
class MessageActionEmpty:
    class Meta:
        name = 'messageAction'


@dataclass
class MessageActionChatAddUser:
    users: List[int]

    class Meta:
        name = 'messageActionChatAddUser'
        order = ('users', )


MessageAction = Annotated[
    Union[MessageActionEmpty, MessageActionChatAddUser],
    'MessageAction'
]


@dataclass
class ChatParticipantCombinator:
    user_id: int
    inviter_id: int
    date: int

    class Meta:
        name = 'chatParticipant'
        order = ('user_id', 'inviter_id', 'date')


@dataclass
class ChatParticipantCreator:
    user_id: int

    class Meta:
        name = 'chatParticipantCreator'
        order = ('user_id', )


@dataclass
class ChatParticipantAdmin:
    user_id: int
    inviter_id: int
    date: int

    class Meta:
        meta = 'chatParticipantAdmin'


ChatParticipant = Annotated[
    Union[
        ChatParticipantCombinator,
        ChatParticipantCreator,
        ChatParticipantAdmin
    ],
    'ChatParticipant'
]


@dataclass
class ChatParticipants:
    chat_id: int
    participants: List[ChatParticipant]
    version: int

    class Meta:
        name = 'chatParticipants'
        order = ('chat_id', 'participants', 'version')


@dataclass
class InputMediaPhotoExternal:
    url: str
    ttl_seconds: Optional[int] = field(metadata={'flag': 0})

    class Meta:
        name = 'inputMediaPhotoExternal'
        order = ('url', 'ttl_seconds')


@dataclass
class InputMediaGifExternal:
    url: str
    q: str

    class Meta:
        name = 'inputMediaGifExternal'


InputMedia = Annotated[
    Union[InputMediaPhotoExternal, InputMediaGifExternal],
    'InputMedia'
]


@dataclass
class DialogFilter:
    class Meta:
        name = 'dialogFilter'


@dataclass
class UpdateDialogFilter:
    id: int
    filter: Optional[DialogFilter] = field(metadata={'flag': 0})

    class Meta:
        name = 'updateDialogFilter'
        order = ('id', 'filter')


@dataclass
class UpdateConfig:
    class Meta:
        name = 'updateConfig'


Update = Annotated[
    Union[UpdateConfig, UpdateDialogFilter],
    'Update'
]


@dataclass
class ExtendedTree:
    val: int
    left: Optional['ExtendedTree'] = field(metadata={'flag': 0})
    right: Optional['ExtendedTree'] = field(metadata={'flag': 1})

    class Meta:
        name = 'extendedTree'
        order = ('val', 'left', 'right')


@dataclass
class WithoutFlags:
    val: Optional[int]

    class Meta:
        name = 'withoutFlags'
        order = ('val', )


@dataclass
class WrongConstructorUsed:
    val: Optional[AnotherClass] = field(metadata={'flag': 0})

    class Meta:
        name = 'withoutFlags'
        order = ('val', )


@dataclass
class IncorrectNoMetaCombinator:
    pass


@dataclass
class Content:
    content: str


@dataclass
class ContentWrapper:
    content: Content = field(metadata={
        'bare': '%',
    })

    class Meta:
        name = 'contentWrapper'
        order = ('content', )


@dataclass
class ContentWrapperLower:
    content: Content = field(metadata={
        'bare': 'lower'
    })

    class Meta:
        name = 'contentWrapperLower'
        order = ('content', )


@dataclass
class ContentList:
    content_list: List[Content] = field(metadata={
        'bare': 'lower',
        'item_meta': {
            'bare': '%'
        }
    })

    class Meta:
        name = 'contentList'
        order = ('content_list', )


@dataclass
class ContentLowerList:
    content_list: List[Content] = field(metadata={
        'bare': 'lower',
        'item_meta': {
            'bare': 'lower'
        }
    })

    class Meta:
        name = 'contentLowerList'
        order = ('content_list', )


@dataclass
class Message:
    msg_id: long
    seqno: int
    bytes: int
    body: Any

    class Meta:
        name = 'message'
        order = (
            'msg_id',
            'seqno',
            'bytes',
            'body',
        )


@dataclass
class MessageContainer:
    messages: List[Message] = field(
        metadata={
            'bare': 'lower',
            'item_meta': {
                'bare': '%'
            }
        }
    )

    class Meta:
        name = 'msg_container'
        order = ('messages',)


async def equals(request: Request, a: int, b: int) -> Bool:  # pragma: nocover
    if a == b:
        return BoolTrue()
    return BoolFalse()


async def get_task_content(
    request: Request,
    task: Task
) -> str:  # pragma: nocover
    return task.content


async def has_tasks(
    request: Request,
    tasks: List[Task]
) -> Bool:  # pragma: nocover
    if len(tasks) > 0:
        return BoolTrue()
    return BoolFalse()


def not_async_func(
    request: Request,
    a: int,
    b: int
) -> Bool:  # pragma: nocover
    if a == b:
        return BoolTrue()
    return BoolFalse()


async def invalid_param(
    request: Request,
    a: AnotherClass,
    b: int
) -> Bool:  # pragma: nocover
    if str(a) == str(b):
        return BoolTrue()
    return BoolFalse()


async def invalid_return_type(
    request: Request,
    a: int,
    b: int
) -> AnotherClass:  # pragma: nocover
    return AnotherClass(a, b)


async def invalid_not_annotated_params(
    request: Request,
    a,
    b
) -> Bool:  # pragma: nocover
    if a == b:
        return BoolTrue()
    return BoolFalse()


async def invalid_args(
    request: Request,
    *args: List[Task]
) -> Bool:  # pragma: nocover
    if len(args) > 0:
        return BoolTrue()
    return BoolFalse()


async def invalid_kwargs(
    request: Request,
    **kwargs
) -> Bool:  # pragma: nocover
    if 'value' in kwargs:
        return BoolTrue()
    return BoolFalse()


async def func_no_request(task: Task) -> Bool:  # pragma: nocover
    return BoolTrue()


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
        left_node_type = TreeNode.__dataclass_fields__['left_node'].type
        assert is_good_for_combinator(left_node_type, [Bool, Tree])

    def test_wrong_value(self):
        assert not is_good_for_combinator(AnotherClass)

    def test_wrong_forward_ref(self):
        assert not is_good_for_combinator(ForwardRef('Tree'), [Bool])

    def test_options_list(self):
        assert is_good_for_combinator(Optional[List[str]])
        assert is_good_for_combinator(
            Optional[List[Task]],
            constructors=[Task]
        )

    def test_any_combinator(self):
        assert is_good_for_combinator(Any)

    def test_combinator_with_bare_type(self):
        assert is_good_for_combinator(
            ContentWrapper,
            [
                ContentWrapper,
                Content
            ]
        )


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
        is_valid_combinator(User)

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
        is_valid_combinator(ChatParticipants, [ChatParticipant])

    def test_valid_optional_base_type_field(self):
        is_valid_combinator(InputMediaPhotoExternal)

    def test_invalid_declared_optional_field(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(WithoutFlags)

    def test_valid_optional_constructor_field(self):
        is_valid_combinator(UpdateDialogFilter, [Update, DialogFilter])
        is_valid_combinator(ExtendedTree, [ExtendedTree])

    def test_valid_optional_list_field(self):
        is_valid_combinator(TaggedTask, [Bool, TaggedTask])

    def test_invalid_not_constructor_optional_field(self):
        with pytest.raises(InvalidCombinator):
            is_valid_combinator(WrongConstructorUsed)

    def test_valid_with_any_field(self):
        is_valid_combinator(RpcResult, [RpcResult])


class TestIsValidConstructor:

    def test_single_combinator(self):
        is_valid_constructor(User)

    def test_union_of_combinators(self):
        is_valid_constructor(Bool, [Bool, Tree])
        is_valid_constructor(Tree, [Bool, Tree])
        is_valid_constructor(ExtendedTree, [ExtendedTree])
        is_valid_constructor(RpcResult, [RpcResult])
        is_valid_constructor(ContentWrapper, [Content])

    def test_wrong_value(self):
        with pytest.raises(InvalidConstructor):
            is_valid_constructor(int)


class TestIsValidFunction:

    def test_valid_with_basic_params(self):
        is_valid_function(equals, [Bool])

    def test_valid_with_constructor_params(self):
        is_valid_function(get_task_content, [Task])

    def test_valid_list_params(self):
        is_valid_function(has_tasks, [Task, Bool])

    def test_not_async_function(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(not_async_func, [Bool])

    def test_invalid_param(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(invalid_param, [Bool])

    def test_invalid_no_constructor(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(equals)

    def test_invalid_return_type(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(invalid_return_type)

    def test_not_annotaed_param(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(invalid_not_annotated_params, [Bool])

    def test_invalid_args(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(invalid_args, [Bool, Task])

    def test_invalid_kwargs(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(invalid_kwargs)

    def test_request_object_does_not_passed(self):
        with pytest.raises(InvalidFunction):
            is_valid_function(func_no_request)


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
        assert build_combinator_description(User, User) == (
            'user id:int name:string = User'
        )

    def test_recursive_combinator(self):
        assert build_combinator_description(Task, Task) == (
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
            for_type_number=True
        ) == 'messageActionChatAddUser users:Vector int = MessageAction'

    def test_list_chat_participants(self):
        assert build_combinator_description(
            ChatParticipants,
            ChatParticipants
        ) == 'chatParticipants chat_id:int participants:Vector<ChatParticipant> version:int = ChatParticipants'  # noqa
        assert build_combinator_description(
            ChatParticipants,
            ChatParticipants,
            for_type_number=True
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
            ExtendedTree,
            ExtendedTree
        ) == 'extendedTree flags:# val:int left:flags.0?ExtendedTree right:flags.1?ExtendedTree = ExtendedTree'  # noqa

    def test_optional_list_field(self):
        assert build_combinator_description(
            TaggedTask,
            TaggedTask
        ) == 'taggedTask flags:# content:string finished:Bool tags:flags.1?Vector<string> = TaggedTask'  # noqa

        assert build_combinator_description(
            TaggedTask,
            TaggedTask,
            for_type_number=True,
        ) == 'taggedTask flags:# content:string finished:Bool tags:flags.1?Vector string = TaggedTask'  # noqa

    def test_res_pq_with_bytes(self):
        assert build_combinator_description(
            ResPQ,
            ResPQ
        ) == 'resPQ nonce:int128 server_nonce:int128 pq:bytes server_public_key_fingerprints:Vector<long> = ResPQ'  # noqa
        assert build_combinator_description(
            ResPQ,
            ResPQ,
            for_type_number=True
        ) == 'resPQ nonce:int128 server_nonce:int128 pq:string server_public_key_fingerprints:Vector long = ResPQ'  # noqa

    def test_rpc_result(self):
        assert build_combinator_description(
            RpcResult, RpcResult
        ) == 'rpc_result req_msg_id:long result:Object = RpcResult'

    def test_bare_constructor_type_content_wrapper(self):
        assert build_combinator_description(
            ContentWrapper,
            ContentWrapper
        ) == 'contentWrapper content:%Content = ContentWrapper'

    def test_bare_constructor_type_content_lower_wrapper(self):
        assert build_combinator_description(
            ContentWrapperLower,
            ContentWrapperLower
        ) == 'contentWrapperLower content:content = ContentWrapperLower'

    def test_bare_constructor_type_content_list(self):
        assert build_combinator_description(
            ContentList,
            ContentList
        ) == 'contentList content_list:vector<%Content> = ContentList'

    def test_bare_constructor_type_content_list_lower(self):
        assert build_combinator_description(
            ContentLowerList,
            ContentLowerList
        ) == 'contentLowerList content_list:vector<content> = ContentLowerList'

    def test_message_container(self):
        assert build_combinator_description(
            MessageContainer,
            MessageContainer
        ) == 'msg_container messages:vector<%Message> = MessageContainer'


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
            ChatParticipants,
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

    def test_rpc_result(self):
        assert get_combinator_number(RpcResult, RpcResult) == 0xf35c6d01

    def test_msg_container(self):
        assert get_combinator_number(
            MessageContainer,
            MessageContainer
        ) == 1945237724


class TestBuildFunctionDescription:

    def test_equals(self):
        assert build_function_description(equals) == (
            'equals a:int b:int = Bool'
        )

    def test_get_task_content(self):
        assert build_function_description(get_task_content) == (
            'get_task_content task:Task = string'
        )

    def test_has_tasks(self):
        assert build_function_description(has_tasks) == (
            'has_tasks tasks:Vector<Task> = Bool'
        )
        assert build_function_description(
            has_tasks,
            for_type_number=True
        ) == 'has_tasks tasks:Vector Task = Bool'


class TestGetFunctionNumber:

    def test_equals(self):
        assert get_function_number(equals) == 0xb5fffb56

    def test_get_task_content(self):
        assert get_function_number(get_task_content) == 0x2e08ac72

    def test_has_tasks(self):
        assert get_function_number(has_tasks) == 0x20e13fab


class TestGetFieldsMap:

    def test_fields_map(self):
        fields_map = get_fields_map(User)

        assert 'id' in fields_map
        assert 'name' in fields_map

    def test_fields_map_typeerror(self):
        with pytest.raises(TypeError):
            get_fields_map(44)
