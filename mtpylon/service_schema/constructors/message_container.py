# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from mtpylon.service_schema.constructors.message import Message


@dataclass
class MessageContainer:
    messages: List[Message]

    class Meta:
        name = 'msg_container'
        order = ('messages',)
