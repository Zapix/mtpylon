# -*- coding: utf-8 -*-
import pytest

from mtpylon.crypto.random_prime import (
    random_odd,
    is_low_level_test_passed,
    is_miller_rabin_passed,
    random_prime
)


prime_tests = [
    (4, False),
    (7, True),
    (10, False),
    (53, True),
    (23438, False),
    (1201, True),
    (7853, True),
    (121231303, True),
    (121231304, False),
    (121234591, True),
]


def test_random_odd():
    value = random_odd(64)

    assert value % 2 == 1
    assert value >> 64 == 1


@pytest.mark.parametrize(
    'value,expected',
    prime_tests,
    ids=lambda x: x
)
def test_is_low_level_test_passed(value, expected):
    assert is_low_level_test_passed(value) == expected


@pytest.mark.parametrize(
    'value,expected',
    prime_tests,
    ids=lambda x: x
)
def test_is_miller_rabin_passed(value, expected):
    assert is_miller_rabin_passed(value) == expected


@pytest.mark.parametrize(
    'n_bits',
    [64, 128, 1024],
    ids=lambda x: x
)
def test_random_prime(n_bits):
    prime = random_prime(n_bits)

    assert prime % 2 == 1
    assert prime >> n_bits == 1
