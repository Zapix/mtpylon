# -*- coding: utf-8 -*-
from mtpylon.income_message import IncomeMessage

from .types import HandleStrategy
from .handle_unknown_message import handle_unknown_message
from .handle_unencrypted_message import handle_unencrypted_message
from .handle_rpc_query_message import handle_rpc_query_message
from .utils import is_unencrypted_message, is_rpc_call_message


def get_handle_strategy(message: IncomeMessage) -> HandleStrategy:
    """
    Selects how message will be handled by message
    """
    if is_unencrypted_message(message):
        return handle_unencrypted_message

    if is_rpc_call_message(message):
        return handle_rpc_query_message

    return handle_unknown_message
