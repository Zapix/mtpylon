# -*- coding: utf-8 -*-
from typing import Any, Callable, Coroutine
from mypy_extensions import Arg, KwArg

from aiohttp.web import Request

Handler = Callable[
    [
        Arg(Request, 'request'),  # noqa: F821
        KwArg(Any)
    ],
    Coroutine[Any, Any, Any]
]

MiddleWareFunc = Callable[
    [
        Arg(Handler, 'handler'),  # noqa: F821
        Arg(Request, 'request'),  # noqa: F821
        KwArg(Any)
    ],
    Coroutine[Any, Any, Any]
]
