# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from mtpylon.service_schema.constructors.message import Message


@dataclass
class MessageContainer:
    messages: List[Message] = field(
        metadata={
            'bare': 'lower',
            'item_meta': {
                'bare': '%'
            }
        }
    )

    class Meta:
        name = 'msg_container'
        order = ('messages',)
