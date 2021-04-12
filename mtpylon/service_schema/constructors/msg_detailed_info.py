# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import long


@dataclass
class MessageDetailedInfo:
    msg_id: long
    answer_msg_id: long
    bytes: int
    status: int

    class Meta:
        name = 'msg_detailed_info'
        order = ('msg_id', 'answer_msg_id', 'bytes', 'status')


@dataclass
class MessageNewDetailedInfo:
    answer_msg_id: long
    bytes: int
    status: int

    class Meta:
        name = 'msg_new_detailed_info'
        order = ('answer_msg_id', 'bytes', 'status')


MsgDetailedInfo = Annotated[
    Union[
        MessageDetailedInfo,
        MessageNewDetailedInfo
    ],
    'MsgDetailedInfo'
]
