# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union, List, Optional

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
    avatar_url: Optional[str]

    class Meta:
        name = 'authorizedUser'
        order = ('id', 'username', 'password', 'avatar_url')
        flags = {
            'avatar_url': 0
        }


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
        password=password,
        avatar_url=None
    )


async def login(username: str, password: str) -> User:
    if username == 'zapix' and password == '123123':
        return AuthorizedUser(
            id=1,
            username=username,
            password=password,
            avatar_url=None
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
