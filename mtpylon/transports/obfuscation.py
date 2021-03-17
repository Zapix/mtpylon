# -*- coding: utf-8 -*-
from typing import Tuple
from dataclasses import dataclass

import pyaes  # type: ignore


@dataclass
class Obfuscator:
    """
    Obfuscator for mtproto transport protocol.
    Stores aes key/iv for client and server.
    Provides `decrypt` method to decrypt client messages
    Provides `encrypt` method to encrypt server messages
    """
    client_key: bytes
    client_iv: bytes

    server_key: bytes
    server_iv: bytes

    def __post_init__(self):
        self._decipher = pyaes.AESModeOfOperationCTR(
            self.client_key,
            counter=pyaes.Counter(int.from_bytes(self.client_iv, 'big'))
        )

        self._cipher = pyaes.AESModeOfOperationCTR(
            self.server_key,
            counter=pyaes.Counter(int.from_bytes(self.server_iv, 'big'))
        )

    def decrypt(self, encrypted_message: bytes) -> bytes:
        return self._decipher.decrypt(encrypted_message)

    def encrypt(self, original_message: bytes) -> bytes:
        return self._cipher.encrypt(original_message)


def parse_header(header: bytes) -> Tuple[int, Obfuscator]:
    """
    Parse incoming header to retrieve client/server aes key iv and
    transport protocol version that should be used.
    Returns transport protocol tag and obfuscator
    """
    client_key = header[8:40]
    client_iv = header[40:56]

    reversed_header = header[::-1]
    server_key = reversed_header[8:40]
    server_iv = reversed_header[40:56]

    obfuscator = Obfuscator(client_key, client_iv, server_key, server_iv)

    encrypted_key = obfuscator.decrypt(header)

    return int.from_bytes(encrypted_key[56:60], 'big'), obfuscator
