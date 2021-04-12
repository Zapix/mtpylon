# -*- coding: utf-8 -*-
from typing import Any
from dataclasses import dataclass

from aiohttp.web import WebSocketResponse

from .transports import Obfuscator, TransportWrapper
from .schema import Schema


@dataclass
class MessageSender:

    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    ws: WebSocketResponse

    async def send_message(self, data: Any) -> None:
        ...
