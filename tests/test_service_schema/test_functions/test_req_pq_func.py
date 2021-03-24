# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock
from contextlib import ExitStack

import pytest

from mtpylon import int128, long
from mtpylon.contextvars import (
    server_nonce,
    p,
    q,
    pq,
    rsa_manager
)
from mtpylon.service_schema.functions import req_pq

from tests.simple_manager import manager


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
