# -*- coding: utf-8 -*-
from dataclasses import dataclass

from mtpylon import long


@dataclass
class NewSession:
    first_msg_id: long
    unique_id: long
    server_salt: long

    class Meta:
        name = 'new_session_created'
        order = (
            'first_msg_id',
            'unique_id',
            'server_salt',
        )
