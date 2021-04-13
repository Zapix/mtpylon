# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated, Union

from mtpylon import long


@dataclass
class BadMessageNotification:
    bad_msg_id: long
    bad_msg_seqno: int
    error_code: int

    class Meta:
        name = 'bad_msg_notification'
        order = (
            'bad_msg_id',
            'bad_msg_seqno',
            'error_code',
        )


@dataclass
class BadServerSalt:
    bad_msg_id: long
    bad_msg_seqno: int
    error_code: int
    new_server_salt: long

    class Meta:
        name = 'bad_server_salt'
        order = (
            'bad_msg_id',
            'bad_msg_seqno',
            'error_code',
            'new_server_salt',
        )


BadMsgNotification = Annotated[
    Union[
        BadMessageNotification,
        BadServerSalt
    ],
    'BadMsgNotification'
]
