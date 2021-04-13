# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import long


@dataclass
class RpcAnswerUnknown:
    class Meta:
        name = 'rpc_answer_unknown'


@dataclass
class RpcAnswerDroppedRunning:
    class Meta:
        name = 'rpc_answer_dropped_running'


@dataclass
class RpcAnswerDropped:
    msg_id: long
    seq_no: int
    bytes: int

    class Meta:
        name = 'rpc_answer_dropped'
        order = ('msg_id', 'seq_no', 'bytes')


RpcDropAnswer = Annotated[
    Union[
        RpcAnswerUnknown,
        RpcAnswerDroppedRunning,
        RpcAnswerDropped,
    ],
    'RpcDropAnswer'
]
