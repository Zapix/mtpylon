# -*- coding: utf-8 -*-
import pytest
from rsa import PublicKey, PrivateKey  # type: ignore

from tests.simple_manager import manager as rsa_manager, key_data_list


@pytest.mark.parametrize(
    'key_data',
    key_data_list,
    ids=lambda x: x.fingerprint
)
def test_contians_fingerprint(key_data):
    assert key_data.fingerprint in rsa_manager


@pytest.mark.parametrize(
    'key_data',
    key_data_list,
    ids=lambda x: x.fingerprint
)
def test_get_keypair(key_data):
    public = PublicKey.load_pkcs1(key_data.public_str)
    private = PrivateKey.load_pkcs1(key_data.private_str)

    key_pair = rsa_manager[key_data.fingerprint]
    assert key_pair.public == public
    assert key_pair.private == private


@pytest.mark.parametrize(
    'key_data',
    key_data_list,
    ids=lambda x: x.public_str
)
def test_check_public_str(key_data):
    public = PublicKey.load_pkcs1(key_data.public_str)
    public_bytes = public.save_pkcs1()
    assert public_bytes in rsa_manager.public_key_list


@pytest.mark.parametrize(
    'key_data',
    key_data_list,
    ids=lambda x: x.fingerprint
)
def test_check_fingerprint_in_list(key_data):
    assert key_data.fingerprint in rsa_manager.fingerprint_list
