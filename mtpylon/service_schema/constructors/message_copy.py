# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon.service_schema.constructors.message import Message


@dataclass
class MessageCopy:
    orig_message: Message

    class Meta:
        name = 'msg_copy'
        order = ('orig_message',)
