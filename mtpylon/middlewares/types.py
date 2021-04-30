# -*- coding: utf-8 -*-
from typing import Any, Callable, Awaitable


MiddleWareFunc = Callable[..., Awaitable[Any]]
