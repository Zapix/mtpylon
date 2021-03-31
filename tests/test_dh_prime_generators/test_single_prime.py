# -*- coding: utf-8 -*-
import pytest

from mtpylon.dh_prime_generators.single_prime import generate, DH_PRIME


@pytest.mark.asyncio
async def test_generate():
    gen = generate()

    assert await gen.asend(None) == DH_PRIME
    assert await gen.asend(None) == DH_PRIME
