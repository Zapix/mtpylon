# -*- coding: utf-8 -*-
def hexstr_to_bytes(value: str) -> bytes:
    return int(value, 16).to_bytes(len(value) // 2, 'big')


def bytes_to_hexstr(value: bytes) -> str:
    return '{0:0x}'.format(int.from_bytes(value, 'big'))
