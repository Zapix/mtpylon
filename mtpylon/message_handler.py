# -*- coding: utf-8 -*-
from dataclasses import dataclass

from .schema import Schema
from .transports import Obfuscator, TransportWrapper
from .message_sender import MessageSender


@dataclass
class MessageHandler:
    schema: Schema
    obfuscator: Obfuscator
    transport_wrapper: TransportWrapper
    message_sender: MessageSender

    async def handle(self, obfuscated_data: bytes):
        ...
