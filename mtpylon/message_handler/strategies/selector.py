# -*- coding: utf-8 -*-
from functools import partial
from mtpylon.income_message import IncomeMessage

from .types import HandleStrategy
from .handle_unknown_message import handle_unknown_message
from .handle_unencrypted_message import handle_unencrypted_message
from .handle_rpc_query_message import handle_rpc_query_message
from .handle_message_container import handle_message_container
from .handle_msgs_ack_message import handle_msgs_ack
from .utils import (
    is_unencrypted_message,
    is_rpc_call_message,
    is_container_message,
    is_msgs_ack
)


def get_handle_strategy(message: IncomeMessage) -> HandleStrategy:
    """
    Selects how message will be handled by message
    """
    if is_unencrypted_message(message):
        return handle_unencrypted_message

    if is_rpc_call_message(message):
        return handle_rpc_query_message

    if is_container_message(message):
        return partial(
            handle_message_container,
            get_handle_strategy
        )

    if is_msgs_ack(message):
        return handle_msgs_ack

    return handle_unknown_message
