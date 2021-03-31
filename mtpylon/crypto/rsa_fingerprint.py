# -*- coding: utf-8 -*-
import math
import hashlib

from rsa import PublicKey  # type: ignore

from mtpylon import long
from mtpylon.serialization.bytes import dump as dump_bytes


def get_len_in_bytes(value: int) -> int:
    """
    Returns minimum length in bytes to dump integer number
    """
    return math.ceil(len("{0:0x}".format(value)) / 2)


def num_to_bytes(value: int) -> bytes:
    """
    Returns num in bytes in big endian order
    """
    return value.to_bytes(get_len_in_bytes(value), 'big')


def num_to_tl_bytes(value: int) -> bytes:
    """
    Dump bytes as tl string
    """
    return dump_bytes(num_to_bytes(value))


def get_fingerprint(key: PublicKey) -> long:
    """
    Builds fingerprint for RSA public key

    Fingerprint is 64 lower-order bits of SHA1 (server_public_key);
    the public key is represented as a bare type:
    rsa_public_key n:string e:string = RSAPublicKey
    """
    res = num_to_tl_bytes(key.n) + num_to_tl_bytes(key.e)
    h = hashlib.sha1(res)
    return long(int.from_bytes(h.digest()[-8:], 'little'))
