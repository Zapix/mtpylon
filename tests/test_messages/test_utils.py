# -*- coding: utf-8 -*-
import pytest

from mtpylon.types import long
from mtpylon.messages.utils import (
    is_encrypted_message,
    is_unencrypted_message,
    message_ids
)

unencrypted_message = (
    b'\x00\x00\x00\x00\x00\x00\x00\x00' +
    b'\x4a\x96\x70\x27\xc4\x7a\xe5\x51' +
    b'\x14\x00\x00\x00' +
    b'\x78\x97\x46\x60' +
    b'\x3e\x05\x49\x82\x8c\xca\x27\xe9\x66\xb3\x01\xa4\x8f\xec\xe2\xfc'
)

encrypted_message = (
    b'\x28\x43\x00\x00\x00\x00\x00\x00' +
    b'\x4a\x96\x70\x27\xc4\x7a\xe5\x51' +
    b'\x14\x00\x00\x00' +
    b'\x78\x97\x46\x60' +
    b'\x3e\x05\x49\x82\x8c\xca\x27\xe9\x66\xb3\x01\xa4\x8f\xec\xe2\xfc'
)


@pytest.mark.parametrize(
    'dumped_message,value',
    [
        pytest.param(
            unencrypted_message,
            False,
            id='unencrypted_message'
        ),
        pytest.param(
            encrypted_message,
            True,
            id='encrypted_message'
        ),
    ]
)
def test_is_encrypted_message(dumped_message, value):
    assert is_encrypted_message(dumped_message) == value


@pytest.mark.parametrize(
    'dumped_message,value',
    [
        pytest.param(
            unencrypted_message,
            True,
            id='unencrypted_message'
        ),
        pytest.param(
            encrypted_message,
            False,
            id='encrypted_message'
        ),
    ]
)
def test_is_unencrypted_message(dumped_message, value):
    assert is_unencrypted_message(dumped_message) == value


def test_message_ids_generator():
    gen = message_ids()
    init_value = gen.send(None)

    assert init_value == long(0)

    message_id = gen.send(True)

    assert message_id % 4 == 1

    response_id = gen.send(True)

    assert response_id % 4 == 1

    assert response_id > message_id

    notification_id = gen.send(None)

    assert notification_id % 4 == 3
    assert message_id < response_id < notification_id
