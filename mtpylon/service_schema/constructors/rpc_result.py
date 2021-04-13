# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any

from mtpylon import long


@dataclass
class RpcResult:
    req_msg_id: long
    result: Any

    class Meta:
        name = 'rpc_result'
        order = ('req_msg_id', 'result')
