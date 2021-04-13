# -*- coding: utf-8 -*-
from .transport_wrapper import TransportWrapper
"""
    Intermediate payload structure is:

    +----+----...----+
    +len.+  payload  +
    +----+----...----+

    Payloads are wrapped in the following envelope:

    - Length: payload length encoded as 4 length bytes (little endian)
    - Payload: the MTProto payload
"""
PROTOCOL_TAG = 0xeeeeeeee


def wrap(buffer: bytes) -> bytes:
    return len(buffer).to_bytes(4, 'little') + buffer


def unwrap(buffer: bytes) -> bytes:
    tlen = int.from_bytes(buffer[:4], 'little')
    return buffer[4:tlen + 4]


wrapper = TransportWrapper(
    PROTOCOL_TAG,
    wrap,
    unwrap
)
