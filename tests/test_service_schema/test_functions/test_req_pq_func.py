# -*- coding: utf-8 -*-
from dataclasses import dataclass
from unittest.mock import patch, MagicMock
from contextlib import ExitStack

import pytest

import rsa  # type: ignore

from mtpylon import int128, long
from mtpylon.crypto import RsaManager, KeyPair
from mtpylon.contextvars import (
    server_nonce,
    p,
    q,
    pq,
    rsa_manager
)
from mtpylon.service_schema.functions import req_pq


@dataclass
class KeyData:
    public_str: str
    private_str: str
    fingerprint: int


key_data_list = [
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQCI0n6BN93gjdBy2TpT6bVlCocwtAktdJZIQkV8Wq6Mj6UrxsdTmdcMB1IO
        94eCnn9fiqu1vW0/TQ7znVCSGiOPAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBOwIBAAJBAIjSfoE33eCN0HLZOlPptWUKhzC0CS10lkhCRXxaroyPpSvGx1OZ
        1wwHUg73h4Kef1+Kq7W9bT9NDvOdUJIaI48CAwEAAQJAd5NfNBdbNjE6h+UJcOTD
        v3agCBSQIMXPwX8Js1Cc1ujvsM7OT2k9PpXDDjmLTt9sMjojn7J3+RswhO+dnK+N
        gQIjAI8lQeYe8zgGNQuuH3YhDH+YltzliA0Kbg5JmuUmFUSX1D8CHwD0sQU/p8JM
        EU6/TacQA3/PUuvOHqjEMUfD5oW2nLECImGrHieRfon/UjpB+B11tz1oM6dMxWOA
        dk8xUYqATYqbvakCHl5bROLfFhWvNuaeUyXhs4+HMlcxi3LcbgglBLr+gQIiUKGF
        hIa7d4vHIPPflSd0GRsdJ8bmY0rJjB4qWXiav0xgHA==
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=13923728974697425819
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQC07rGil6ujqOwn2fbrHRbkjmUkg3kafl81F6NfmA4+GpZ058QnYzZVaH8F
        ISC4ZcggmJ+bnnFzZS5HXVnPS2ElAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBPQIBAAJBALTusaKXq6Oo7CfZ9usdFuSOZSSDeRp+XzUXo1+YDj4alnTnxCdj
        NlVofwUhILhlyCCYn5uecXNlLkddWc9LYSUCAwEAAQJAb3PBdHidQBkkL4Aye63V
        lkCoyQ87oDhMCXZgKtiNGItqAWkVVpx8LyDC79o7nldmTVJXEeJ9idOCC3FGgLhc
        mQIjANe9GaNKQyH/bjTATpv1F6/3O5cmdqSwNxH1KoQvBA8EoCcCHwDWsrn3iuxi
        ucKqkuPcdzm0sN7sz63elUpLQHg1N9MCIwCkpvxENc9ayTnxJLxaJwq3D/f4+jAe
        rSa6m+ShEckFNUCNAh4iBxOoYzFR+GUdCcjpgU/5DmtWlxfUhk7PHHmw3ZcCIwDB
        j7pPPfkOdQmWybZxk19n3309S2Tf/OM411Da3S3m5Cix
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=2244281079002705184
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQCS2U07TIBID7KzsNc3pa1yCxnhvXG1uSluJE86HMAhjr8IXh7M3x3J3liE
        y/JeJgVdZQ8J+c7jm6HcFlc3fkjZAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBPAIBAAJBAJLZTTtMgEgPsrOw1zelrXILGeG9cbW5KW4kTzocwCGOvwheHszf
        HcneWITL8l4mBV1lDwn5zuObodwWVzd+SNkCAwEAAQJAHQBbd12ZbCHligVfy7al
        tYMpvmJapagG3aDAINrynXGM5IvrIkBRzBVdnvogauu6FW1qoF7UdLZm++VYvDPZ
        nQIjAJVNHNvQilc53gvSLAo3E+IMm/yOcpFFTFb/0Ex0Vyg6kbsCHwD7y4Vhcg1g
        xkYXzGfh2izPQJokdnQa8cZ0KOR4jHsCIndDDP1uPUPmHsB0l+dlDcXxap05ML1o
        jM2mNT8NZB3ng0cCHwDF99szpV99Uga0GWMnwMjwXkOTHYrl0GgO1kPjv9cCIm6I
        v3q7L38lqQ7um1ycT7QY8Sh4SfX/HFdcTPe1dnDUhvE=
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=5339281804123932840
    )
]

key_pairs = [
    KeyPair(
        public=rsa.PublicKey.load_pkcs1(item.public_str),
        private=rsa.PrivateKey.load_pkcs1(item.private_str),
    )
    for item in key_data_list
]

manager = RsaManager(key_pairs)


@pytest.mark.asyncio
async def test_req_pq():
    nonce_value = int128(88224628713810667588887952107997447839)
    server_nonce_value = int128(235045274609009641577718790092619182246)
    p_value = 1834598767
    q_value = 1932921469
    pq_value = 3546135343735228723

    rsa_manager.set(manager)

    getrandbits = MagicMock(return_value=server_nonce_value)

    random_prime = MagicMock(side_effect=[q_value, p_value])

    with ExitStack() as patcher:
        patcher.enter_context(
            patch(
                'mtpylon.service_schema.functions.req_pq_func.getrandbits',
                getrandbits
            )
        )
        patcher.enter_context(
            patch(
                'mtpylon.service_schema.functions.req_pq_func.random_prime',
                random_prime
            )
        )

        result = await req_pq(nonce_value)

        assert result.nonce == nonce_value
        assert result.server_nonce == server_nonce_value
        assert server_nonce.get() == server_nonce_value

        assert int.from_bytes(result.pq, 'big') == pq_value
        assert int.from_bytes(pq.get(), 'big') == pq_value
        assert p.get() == long(p_value)
        assert q.get() == long(q_value)

        assert len(result.server_public_key_fingerprints) == 1
        fingerprint = result.server_public_key_fingerprints[0]
        assert fingerprint in manager.fingerprint_list
