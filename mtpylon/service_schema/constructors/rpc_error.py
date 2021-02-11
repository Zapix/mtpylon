# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class RpcError:
    error_code: int
    error_message: str

    class Meta:
        name = 'rpc_error'
        order = ('error_code', 'error_message')
