# -*- coding: utf-8 -*-
from dataclasses import dataclass
from hashlib import sha1


@dataclass(frozen=True)
class AuthKey:
    value: int

    def __hash__(self) -> int:
        """
        hash truncates to Py_ssize_t value
        """
        return self.hash

    @property
    def hash(self) -> int:
        return int.from_bytes(
            sha1(self.value.to_bytes(256, 'big')).digest(),
            'big'
        )

    @property
    def id(self) -> int:
        return int.from_bytes(
            self.hash.to_bytes(20, 'big')[-8:],
            'big'
        )

    @property
    def aux_hash(self) -> int:
        return int.from_bytes(
            self.hash.to_bytes(20, 'big')[:8],
            'big'
        )
