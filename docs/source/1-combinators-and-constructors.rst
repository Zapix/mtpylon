Combinators and constructors
============================

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
* `flags` - dict strings to int Describes info about flags for options fields and order of it


.. _mtpylon_constructors:

Constructor
-----------

| *Constructor* is a combinator that cannot be computed (reduced). This is used to represent composite data types.

Constructor could be annotated union of combinators with name  or single combinator. See :ref:`mtpylon_combinators`


.. code-block:: python

  from typing import Annotated

  Bool = Annotated[Union[BoolTrue, BoolFalse], 'Bool']

