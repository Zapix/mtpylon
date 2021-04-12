# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Annotated, Union

from mtpylon import long


@dataclass
class MessageResendReq:
    msg_ids: List[long]

    class Meta:
        name = 'msg_resend_req'
        order = ('msg_ids',)


@dataclass
class MessageResendAnsReq:
    msg_ids: List[long]

    class Meta:
        name = 'msg_resend_ans_req'
        order = ('msg_ids', )


MsgResendReq = Annotated[
    Union[
        MessageResendReq,
        MessageResendAnsReq
    ],
    'MsgResendReq'
]
