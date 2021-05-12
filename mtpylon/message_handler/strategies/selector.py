# -*- coding: utf-8 -*-
from mtpylon.messages import MtprotoMessage

from .types import HandleStrategy


def get_handle_strategy(message: MtprotoMessage) -> HandleStrategy:
    """
    Selects how message will be handled by message
    """
    ...
