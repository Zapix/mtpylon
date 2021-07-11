Combinators, constructors and functions
=======================================

.. _mtpylon_combinators:

Combinators
-----------

As described in `telegram documentation <https://core.telegram.org/mtproto/serialize>`_:

| **Combinator** is a function that takes arguments of certain types and returns a value of some other type.
| We normally look at combinators whose argument and result types are data types (rather than functional types).

| *Arity (of combinator)* is a non-negative integer, the number of combinator arguments.

| *Combinator identifier* is an identifier beginning with a lowercase Roman letter that uniquely identifies a combinator.

So we could describe it as dataclass with `class Meta` argument that has name of combinator

.. code-block:: python

   from dataclasses import dataclass

   @dataclass
    class BoolTrue:
        class Meta:
            name = 'boolTrue'


    @dataclass
    class BoolFalse:
        class Meta:
            name = 'boolFalse'


    @dataclass
    class Task:
        content: str
        finished: Bool

        class Meta:
            name = 'task'
            order = ('content', 'finished')

`class Meta` of combinator is a class with information about current type. It containes info about:

* `name` - string. Describes name of combinator
* `order` - tuple of strings. Describes attributes order


Attribute of `combinator` class should be one of :ref:`basic types <mtpylon_basic_types>`, :ref:`constructors <mtpylon_constructors>`,
they could be optional and/or bare type

.. _optional:

Optional fields
^^^^^^^^^^^^^^^

Optional fields is field that could be none for in combinator.
To set field as optional you need:

 * Use `typing.Optional` type for annotating
 * Set flag with index for `dataclass.field()` in `metadata` param index is
   a bit number in `# Type <https://core.telegram.org/type/%23>`_

.. code-block:: python

  @dataclass
  class AuthorizedUser:
      id: int
      username: str
      password: str
      avatar_url: Optional[str] = field(metadata={'flag': 0})

      class Meta:
          name = 'authorizedUser'
          order = ('id', 'username', 'password', 'avatar_url')

.. _bare_type:

Bare types
^^^^^^^^^^

.. note::

  Be aware of using bare types. It used only in a few places
  for service messages. bare types aren't looks safe and stable.

Bare type is a type whose values do not contain a constructor number,
which is implied instead. A bare type identifier always coincides with the
name of the implied constructor (and therefore, begins with a lowercase letter)
For more information check `Mtproto Boxed and Bare Types <https://core.telegram.org/mtproto/serialize#boxed-and-bare-types>`_

To set field as bare you need:

  * Set `bare` param for `dataclass.field()` in `metadata` param. Bare could be
    `"lower"` or `"%"`. This is required for different building tl-string options


.. _mtpylon_constructors:

Constructor
-----------

| *Constructor* is a combinator that cannot be computed (reduced). This is used to represent composite data types.

Constructor could be annotated union of combinators with name  or single combinator. See :ref:`mtpylon_combinators`


.. code-block:: python

  from typing import Annotated

  Bool = Annotated[Union[BoolTrue, BoolFalse], 'Bool']

.. _mtpylon_functions:

Functions
---------

In mtpylon all functions are async and described with annotations. Each paramaters
and return value should be annotated with basic type or :ref:`mtpylon_constructors`
`*expressions` and `**expressions` are not allowed for mtpylon functions

.. code-block:: python

    async def equals(a: int, b: int) -> Bool:
        if a == b:
            return BoolTrue()
        return BoolFalse()
