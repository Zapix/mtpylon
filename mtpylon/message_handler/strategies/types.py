# -*- coding: utf-8 -*-
from typing import Callable, Awaitable, List
from mypy_extensions import Arg

from mtpylon.messages import MtprotoMessage
from mtpylon.middlewares import MiddleWareFunc
from mtpylon.message_sender import MessageSender


HandleStrategy = Callable[
    [
        Arg(List[MiddleWareFunc], 'middlewares'),  # noqa: F821
        Arg(MessageSender, 'sender'),  # noqa: F821
        Arg(MtprotoMessage, 'message'),  # noqa: F821
    ],
    Awaitable[None]
]
