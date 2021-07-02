# -*- coding: utf-8 -*-
from unittest.mock import MagicMock
from random import getrandbits, randbytes
from hashlib import sha1

from tgcrypto import ige256_decrypt  # type: ignore


import pytest

from mtpylon import int128, long, int256
from mtpylon.crypto.rsa_manager import RsaManagerProtocol
from mtpylon.contextvars import (
    server_nonce_var,
    new_nonce_var,
    p_var,
    q_var,
    pq_var,
)
from mtpylon.dh_prime_generators.single_prime import (
    generate as generate_dh,
    DH_PRIME,
)
from mtpylon.service_schema.serialization import dump, load
from mtpylon.service_schema.constructors import (
    PQInnerData,
    ServerDHParamsOk,
    ServerDHParamsFail,
    Server_DH_inner_data
)
from mtpylon.service_schema.functions import req_DH_params
from mtpylon.service_schema.functions.req_DH_params_func import \
    decrypt_inner_data
from mtpylon.service_schema.utils import generate_tmp_key_iv
from mtpylon.utils import dump_integer_big_endian
from mtpylon.crypto.rsa import encrypt as rsa_encrypt
from mtpylon.constants import (
    RSA_MANAGER_RESOURCE_NAME,
    DH_PRIME_GENERATOR_RESOURCE_NAME
)

from tests.simple_manager import manager

nonce_value = int128(88224628713810667588887952107997447839)
server_nonce_value = int128(235045274609009641577718790092619182246)
p_value = 1834598767
q_value = 1932921469
pq_value = 3546135343735228723


def setup_function(function):
    server_nonce_var.set(server_nonce_value)
    p_var.set(p_value)
    q_var.set(q_value)
    pq_var.set(pq_value)


@pytest.fixture
def aiohttp_request():
    """
    Returns mocked aiohttp request
    """
    request = MagicMock()
    request.app = {
        RSA_MANAGER_RESOURCE_NAME: manager,
        DH_PRIME_GENERATOR_RESOURCE_NAME: generate_dh(),
    }

    return request


def encrypt_client_data(
    rsa_manager: RsaManagerProtocol,
    serialized_data: bytes,
    fingerprint: long
) -> bytes:
    data_hash = sha1(serialized_data).digest()
    postfix_size = 255 - 20 - len(serialized_data)

    data_with_hash = data_hash + serialized_data + randbytes(postfix_size)

    key_pair = rsa_manager[fingerprint]

    return rsa_encrypt(data_with_hash, key_pair.public)


def wrong_encrypted_data(
    rsa_manager: RsaManagerProtocol,
    serialized_data: bytes,
    fingerprint: long
) -> bytes:
    data_hash = b'\x00' * 20
    postfix_size = 255 - 20 - len(serialized_data)

    data_with_hash = data_hash + serialized_data + randbytes(postfix_size)

    key_pair = rsa_manager[fingerprint]

    return rsa_encrypt(data_with_hash, key_pair.public)


def test_decrypt_success():
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    raw_data = decrypt_inner_data(manager, encrypted_data, fingerprint)

    assert p_q_inner_data == raw_data


def test_decrypt_fingerprint_doesnot_exist():
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    with pytest.raises(ValueError):
        decrypt_inner_data(manager, encrypted_data, long(123123))


def test_decrypt_wrong_fingerprint():
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    wrong_fingerprint = manager.fingerprint_list[1]

    with pytest.raises(ValueError):
        decrypt_inner_data(
            manager,
            encrypted_data,
            wrong_fingerprint
        )


def test_decrypt_wrong_value_encoded():
    fingerprint = manager.fingerprint_list[0]

    wrong_data = b'it is not encrypted data'
    encrypted_data = encrypt_client_data(manager, wrong_data, fingerprint)

    with pytest.raises(ValueError):
        decrypt_inner_data(manager, encrypted_data, fingerprint)


@pytest.mark.asyncio
async def test_req_DH_params_ok(aiohttp_request):
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    result = await req_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        p_bytes,
        q_bytes,
        fingerprint,
        encrypted_data
    )

    assert isinstance(result, ServerDHParamsOk)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value

    key_iv_pair = generate_tmp_key_iv(result.server_nonce, new_nonce_value)
    unencrypted_data = ige256_decrypt(
        result.encrypted_answer,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    loaded_data = load(unencrypted_data[20:])
    value = loaded_data.value

    assert isinstance(value, Server_DH_inner_data)

    assert value.server_nonce == server_nonce_value
    assert value.nonce == nonce_value
    assert int.from_bytes(value.dh_prime, 'big') == DH_PRIME

    assert new_nonce_value == new_nonce_var.get()


@pytest.mark.asyncio
async def test_req_DH_wront_encrypted_hash(aiohttp_request):
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = wrong_encrypted_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    with pytest.raises(ValueError):
        await req_DH_params(
            aiohttp_request,
            nonce_value,
            server_nonce_value,
            p_bytes,
            q_bytes,
            fingerprint,
            encrypted_data
        )


@pytest.mark.asyncio
async def test_req_DH_fail_p_bytes(aiohttp_request):
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))
    new_nonce_hash_bytes = sha1(
        new_nonce_value.to_bytes(64, 'big')
    ).digest()[-8:]
    new_nonce_hash = int128(int.from_bytes(new_nonce_hash_bytes, 'big'))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(34223423)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    result = await req_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        p_bytes,
        q_bytes,
        fingerprint,
        encrypted_data
    )

    assert isinstance(result, ServerDHParamsFail)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value
    assert result.new_nonce_hash == new_nonce_hash


@pytest.mark.asyncio
async def test_req_DH_fail_wrong_server_nonce(aiohttp_request):
    fingerprint = manager.fingerprint_list[0]

    new_nonce_value = int256(getrandbits(256))

    pq_bytes = dump_integer_big_endian(pq_value)
    p_bytes = dump_integer_big_endian(p_value)
    q_bytes = dump_integer_big_endian(q_value)

    p_q_inner_data = PQInnerData(
        pq=pq_bytes,
        p=p_bytes,
        q=q_bytes,
        nonce=nonce_value,
        server_nonce=int128(12312312312),
        new_nonce=new_nonce_value
    )

    p_q_inner_data_bytes = dump(p_q_inner_data)
    encrypted_data = encrypt_client_data(
        manager,
        p_q_inner_data_bytes,
        fingerprint
    )

    with pytest.raises(ValueError):
        await req_DH_params(
            aiohttp_request,
            nonce_value,
            server_nonce_value,
            p_bytes,
            q_bytes,
            fingerprint,
            encrypted_data
        )
