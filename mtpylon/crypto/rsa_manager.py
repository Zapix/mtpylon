# -*- coding: utf-8 -*-
from typing import Protocol, List, Dict
from dataclasses import dataclass

from rsa import PublicKey, PrivateKey  # type: ignore

from .. import long
from .rsa_fingerprint import get_fingerprint


@dataclass
class KeyPair:
    private: PrivateKey
    public: PublicKey


class RsaManagerProtocol(Protocol):

    def __contains__(self, item: long) -> bool:  # pragma: no cover
        ...

    def __getitem__(self, item: long) -> KeyPair:  # pragma: no cover
        ...

    @property
    def public_key_list(self) -> List[bytes]:  # pragma: no cover
        ...

    @property
    def fingerprint_list(self) -> List[long]:  # pragma: no cover
        ...


class RsaManager(RsaManagerProtocol):

    def __init__(self, rsa_keys: List[KeyPair]):
        self._key_map: Dict[long, KeyPair] = {
            get_fingerprint(item.public): item
            for item in rsa_keys
        }

    def __contains__(self, item: long) -> bool:
        return item in self._key_map

    def __getitem__(self, item: long) -> KeyPair:
        return self._key_map[item]

    @property
    def public_key_list(self) -> List[bytes]:
        return [
            key.public.save_pkcs1()
            for key in self._key_map.values()
        ]

    @property
    def fingerprint_list(self) -> List[long]:
        return [
            long(fingerprint)
            for fingerprint in self._key_map.keys()
        ]
