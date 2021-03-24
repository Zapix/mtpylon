# -*- coding: utf-8 -*-
# flake8: noqa
from unittest.mock import patch, MagicMock
from contextlib import ExitStack

import pytest

from mtpylon import int128, long
from mtpylon.contextvars import (
    server_nonce,
    p_var,
    q_var,
    pq_var,
    rsa_manager
)
from mtpylon.service_schema.functions import req_pq_multi

from tests.simple_manager import manager


@pytest.mark.asyncio
async def test_req_pq_multi():
    nonce_value = int128(88224628713810667588887952107997447839)
    server_nonce_value = int128(235045274609009641577718790092619182246)
    p_value = 1834598767
    q_value = 1932921469
    pq_value = 3546135343735228723

    assert pq_value < (2 ** 63) - 1

    rsa_manager.set(manager)

    getrandbits = MagicMock(return_value=server_nonce_value)

    random_prime = MagicMock(side_effect=[q_value, p_value])

    with ExitStack() as patcher:
        patcher.enter_context(
            patch(
                'mtpylon.service_schema.functions.req_pq_multi_func.getrandbits',  # noqa
                getrandbits
            )
        )
        patcher.enter_context(
            patch(
                'mtpylon.service_schema.utils.random_prime',
                random_prime
            )
        )

        result = await req_pq_multi(nonce_value)

        assert result.nonce == nonce_value
        assert result.server_nonce == server_nonce_value
        assert server_nonce.get() == server_nonce_value

        assert int.from_bytes(result.pq, 'big') == pq_value
        assert pq_var.get() == pq_value
        assert p_var.get() == p_value
        assert q_var.get() == q_value

        assert len(result.server_public_key_fingerprints) > 0

        for fingerprint in result.server_public_key_fingerprints:
            assert fingerprint in manager.fingerprint_list
