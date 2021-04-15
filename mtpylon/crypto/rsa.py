# -*- coding: utf-8 -*-
import rsa  # type: ignore

from mtpylon.utils import bytes_needed


def encrypt(original_data: bytes, public: rsa.PublicKey) -> bytes:
    """
    Rough rsa encrypt implementation only for auth key exchange
    """
    original_value = int.from_bytes(original_data, 'big')

    encrypted_value = pow(original_value, public.e, public.n)

    return encrypted_value.to_bytes(bytes_needed(encrypted_value), 'big')


def decrypt(encrypted_data: bytes, private: rsa.PrivateKey) -> bytes:
    """
    Rough rsa dencrypt implementation only for auth key exchange
    """
    encrypted_value = int.from_bytes(encrypted_data, 'big')

    original_value = pow(encrypted_value, private.d, private.n)

    return original_value.to_bytes(bytes_needed(original_value), 'big')
