# -*- coding: utf-8 -*-
from contextlib import ExitStack
from unittest.mock import patch, MagicMock
from typing import Annotated, Union, List
from dataclasses import dataclass

from mtpylon import Schema


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
class AuthorizedUser:
    id: int
    username: str
    password: str

    class Meta:
        name = 'authorizedUser'
        order = ('id', 'username', 'password')


@dataclass
class AnonymousUser:

    class Meta:
        name = 'anonymousUser'


User = Annotated[Union[AuthorizedUser, AnonymousUser], 'User']


@dataclass
class Task:
    id: int
    content: str
    completed: Bool

    class Meta:
        name = 'task'
        order = ('id', 'content', 'completed')


@dataclass
class TaskList:
    tasks: List[Task]

    class Meta:
        name = 'taskList'
        order = ('tasks', )


async def register(username: str, password: str) -> User:
    return AuthorizedUser(
        id=1,
        username=username,
        password=password
    )


async def login(username: str, password: str) -> User:
    if username == 'zapix' and password == '123123':
        return AuthorizedUser(
            id=1,
            username=username,
            password=password
        )

    return AnonymousUser()


async def set_task(content: str) -> Task:
    return Task(
        id=1,
        content=content,
        completed=BoolFalse()
    )


async def get_task_list() -> TaskList:
    return TaskList(tasks=[
        Task(
            id=1,
            content='Init mtpylon project',
            completed=BoolTrue()
        ),
        Task(
            id=2,
            content='Describe mtpylon schema',
            completed=BoolFalse()
        )
    ])


def test_schema():
    is_valid_constructor = MagicMock()
    is_valid_function = MagicMock()

    with ExitStack() as patcher:
        patcher.enter_context(patch(
            'mtpylon.schema.is_valid_constructor',
            is_valid_constructor
        ))
        patcher.enter_context(patch(
            'mtpylon.schema.is_valid_function',
            is_valid_function
        ))

        Schema(
            constructors=[
                Bool,
                User,
                Task,
                TaskList,
            ],
            functions=[
                register,
                login,
                set_task,
                get_task_list,
            ]
        )

    assert is_valid_constructor.called
    assert is_valid_constructor.call_count == 4
    assert is_valid_function.called
    assert is_valid_function.call_count == 4


schema = Schema(
    constructors=[
        Bool,
        User,
        Task,
        TaskList,
    ],
    functions=[
        register,
        login,
        set_task,
        get_task_list,
    ]
)
