# -*- coding: utf-8 -*-
from typing import Dict

from .transport_wrapper import TransportWrapper
from .intermediate import wrapper as intermediate_wrapper

tranport_map: Dict[int, TransportWrapper] = {
    intermediate_wrapper.protocol_tag: intermediate_wrapper
}


def get_wrapper(protocol_tag: int) -> TransportWrapper:
    """
    Gets transport wrapper by protocol_tag or raise ValueError
    """
    if protocol_tag not in tranport_map:
        raise ValueError(f'Transport tag {hex(protocol_tag)} not found')

    return tranport_map[protocol_tag]
