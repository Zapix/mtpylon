# -*- coding: utf-8 -*-
from typing import Callable, Awaitable, List

from mypy_extensions import Arg
from aiohttp.web import Request


from mtpylon.income_message import IncomeMessage
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.message_sender import MessageSender


HandleStrategy = Callable[
    [
        Arg(List[MiddleWareFunc], 'middlewares'),  # noqa: F821
        Arg(MessageSender, 'sender'),  # noqa: F821
        Arg(Request, 'request'),  # noqa: F821
        Arg(IncomeMessage, 'message'),  # noqa: F821
    ],
    Awaitable[None]
]
