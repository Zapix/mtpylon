# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union, List, Optional

from aiohttp import web

from mtpylon import Schema
from mtpylon.exceptions import RpcCallError


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
    tags: Optional[List[str]]

    class Meta:
        name = 'task'
        order = ('id', 'content', 'completed', 'tags')
        flags = {
            'tags': 1
        }


@dataclass
class TaskList:
    tasks: List[Task]

    class Meta:
        name = 'taskList'
        order = ('tasks', )


async def register(request: web.Request, username: str, password: str) -> User:
    return AuthorizedUser(
        id=1,
        username=username,
        password=password,
        avatar_url=None
    )


async def login(request: web.Request, username: str, password: str) -> User:
    if username == 'zapix' and password == '123123':
        return AuthorizedUser(
            id=1,
            username=username,
            password=password,
            avatar_url=None
        )

    return AnonymousUser()


async def set_task(request: web.Request, content: str) -> Task:
    return Task(
        id=1,
        content=content,
        completed=BoolFalse(),
        tags=None,
    )


async def get_task_list(request: web.Request) -> TaskList:
    return TaskList(tasks=[
        Task(
            id=1,
            content='Init mtpylon project',
            completed=BoolTrue(),
            tags=None,
        ),
        Task(
            id=2,
            content='Describe mtpylon schema',
            completed=BoolFalse(),
            tags=None,
        )
    ])


async def get_task(request: web.Request, task_id: int) -> Task:
    if task_id == 4:
        raise RpcCallError(
            error_code=404,
            error_message=f'Task with id {task_id} not found'
        )

    if task_id == 3:
        raise ValueError('Value Error')

    return Task(
        id=1,
        content='Init mtpylon project',
        completed=BoolTrue(),
        tags=None,
    )


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
        get_task
    ]
)
