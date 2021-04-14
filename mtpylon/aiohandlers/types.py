# -*- coding: utf-8 -*-
from typing import Callable, Awaitable

from aiohttp.web import Response, Request, WebSocketResponse

RequestHandler = Callable[[Request], Awaitable[Response]]

WebSocketHandler = Callable[[Request], Awaitable[WebSocketResponse]]
