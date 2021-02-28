# -*- coding: utf-8 -*-
from typing import Protocol, List
from dataclasses import dataclass

from rsa import PublicKey, PrivateKey  # type: ignore


@dataclass
class KeyPair:
    private: PrivateKey
    public: PublicKey


class RsaManagerProtocol(Protocol):

    def __contains__(self, item: int) -> bool:
        ...

    def __getitem__(self, item: int) -> KeyPair:
        ...

    def get_public_key_list(self) -> List[str]:
        ...

    def get_fingerprint_list(self) -> List[int]:
        ...
