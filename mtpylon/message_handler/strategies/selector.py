# -*- coding: utf-8 -*-
from mtpylon.messages import MtprotoMessage, UnencryptedMessage

from .types import HandleStrategy
from .handle_unknown_message import handle_unknown_message
from .handle_unencrypted_message import handle_unencrypted_message


def get_handle_strategy(message: MtprotoMessage) -> HandleStrategy:
    """
    Selects how message will be handled by message
    """
    if isinstance(message, UnencryptedMessage):
        return handle_unencrypted_message

    return handle_unknown_message
