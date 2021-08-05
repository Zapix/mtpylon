# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock

from mtpylon.salts.salt import random_long


def test_negative_random_long():
    val = 18446744073709551593
    getrandbits = MagicMock(return_value=val)
    with patch('mtpylon.salts.salt.getrandbits', getrandbits):
        result = random_long()

    assert result == -23
