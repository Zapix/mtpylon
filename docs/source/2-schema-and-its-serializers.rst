Schema and its serializers
==========================

.. _mtpylon_schema:

Schema
------

Schema is a main class that allow dumps, loads messages for mtproto and
returns schema structure that could be used to dump it.
To create schema you need passed valid constructors(See :ref:`mtpylon_constructors`) and
functions(See :ref:`mtpylon_functions`) that will be used in your program.

Example:

.. code-block:: python

  from dataclasses import dataclass
  from typing import Annotated, Union, List

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


.. _mtpytlon_serializers:

Serializers
-----------

You could get schema structure with method `schema.get_schema_structure()` that
allows you to create custom serializers. Mtpylon provides `to_dict`, `to_json`
and `to_tl_program` (`See Tl-language: https://core.telegram.org/mtproto/TL`_ ) serializers by default


.. code-block:: python

  from mtpylon.serializers import to_dict, to_json, to_tl_program

  to_dict(schema)  # returns python dict that could be serialized

  to_json(schema)  # return json representation

  to_tl_program(schema)  # return tl program representation
