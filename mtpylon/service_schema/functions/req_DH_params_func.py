# -*- coding: utf-8 -*-
import logging
from typing import cast
from hashlib import sha1
from datetime import datetime
from random import getrandbits

from aiohttp import web
from tgcrypto import ige256_encrypt  # type: ignore

from mtpylon import Schema, long, int128, int256
from mtpylon.crypto.rsa_manager import RsaManagerProtocol
from mtpylon.contextvars import (
    server_nonce_var,
    new_nonce_var,
    p_var,
    q_var,
    pq_var,
    g_var,
    a_var,
    dh_prime_var,
)
from mtpylon.serialization import LoadedValue
from mtpylon.serialization.schema import load, dump
from mtpylon.crypto.rsa import decrypt as rsa_decrypt
from mtpylon.constants import (
    RSA_MANAGER_RESOURCE_NAME,
    DH_PRIME_GENERATOR_RESOURCE_NAME
)

from ..constructors import (
    Server_DH_Params,
    ServerDHParamsOk,
    ServerDHParamsFail,
    Server_DH_inner_data,
    P_Q_inner_data
)
from ...utils import dump_integer_big_endian
from ..utils import generate_a, generate_g, generate_dh_prime, \
    generate_tmp_key_iv


logger = logging.getLogger('mtpylon.authorization')


def get_servertime():
    return int(datetime.now().timestamp())


def load_pq_inner_data(raw_data: bytes) -> LoadedValue[P_Q_inner_data]:
    tmp_schema = Schema(constructors=[P_Q_inner_data], functions=[])
    loaded_data = load(raw_data, schema=tmp_schema)
    value = loaded_data.value

    value = cast(P_Q_inner_data, value)
    return LoadedValue(value=value, offset=loaded_data.offset)


def dump_dh_inner_data(data: Server_DH_inner_data):
    tmp_schema = Schema(constructors=[Server_DH_inner_data], functions=[])
    return dump(data, schema=tmp_schema, custom_dumpers=None)


def decrypt_inner_data(
        rsa_manager: RsaManagerProtocol,
        encrypted_data: bytes,
        fingerprint: long
) -> P_Q_inner_data:
    if fingerprint not in rsa_manager:
        raise ValueError(f'Fingerprint {fingerprint} not found in manager')

    key_pair = rsa_manager[fingerprint]

    try:
        unencrypted_data = rsa_decrypt(encrypted_data, key_pair.private)
    except OverflowError:
        raise ValueError(f'Can`t decrypt data with fingerprint {fingerprint}')

    loaded_value = load_pq_inner_data(unencrypted_data[20:])
    loaded_hash = sha1(unencrypted_data[20:20 + loaded_value.offset]).digest()

    if unencrypted_data[:20] != loaded_hash:
        raise ValueError('Hash are not equal for inner_pq_data')

    return loaded_value.value


def build_new_nonce_hash(new_nonce: int256) -> int128:
    new_nonce_hash_bytes = sha1(
        new_nonce.to_bytes(64, 'big')
    ).digest()[-8:]
    return int128(int.from_bytes(new_nonce_hash_bytes, 'big'))


def is_valid_pq_params(p: bytes, q: bytes, inner_data: P_Q_inner_data):
    return (
        p == inner_data.p and
        q == inner_data.q and
        int.from_bytes(p, 'big') == p_var.get() and
        int.from_bytes(q, 'big') == q_var.get() and
        int.from_bytes(inner_data.pq, 'big') == pq_var.get()

    )


def prepare_for_encrypt(data: bytes) -> bytes:
    postfix_size = (16 - (len(data) + 20) % 16) % 16

    return (
        sha1(data).digest() +
        data +
        getrandbits(postfix_size).to_bytes(postfix_size, 'big')
    )


async def req_DH_params(
        request: web.Request,
        nonce: int128,
        server_nonce: int128,
        p: bytes,
        q: bytes,
        public_key_fingerprint: long,
        encrypted_data: bytes
) -> Server_DH_Params:
    """
    Requests DH keys exchanges. Checks server_nonce, p q values.
    If p, q values are wront that returns fail info.
    Generates and returns initial DH exchange values:
    g, dh_prime, g_a.

    Raises:
        ValueError - if server_nonce are not equal, or can't decrypt inner data

    Returns:
        ServerDHParamsFail - if p,q value has been wrong computed on client
        ServerDHParamsOK - if p,q values are valid
    """
    logger.info('Handle req DH params')

    inner_data = decrypt_inner_data(
        request.app[RSA_MANAGER_RESOURCE_NAME],
        encrypted_data,
        public_key_fingerprint
    )
    new_nonce_var.set(inner_data.new_nonce)
    logger.debug(f'New nonce: {inner_data.new_nonce}')
    new_nonce_hash = build_new_nonce_hash(inner_data.new_nonce)

    logger.debug(f'Context var server none: {server_nonce_var.get()}')
    logger.debug(f'Server nonce: {server_nonce}')
    logger.debug(f'Server nonce inner: {inner_data.server_nonce}')

    if (
            server_nonce != server_nonce_var.get() or
            server_nonce != inner_data.server_nonce
    ):
        raise ValueError('Wrong server nonces')

    if not is_valid_pq_params(p, q, inner_data):
        logger.error('Wrong server  pq params')
        return ServerDHParamsFail(
            nonce=nonce,
            server_nonce=server_nonce_var.get(),
            new_nonce_hash=new_nonce_hash
        )

    dh_prime = await generate_dh_prime(
        request.app[DH_PRIME_GENERATOR_RESOURCE_NAME]
    )
    dh_prime_var.set(dh_prime)

    g = await generate_g()
    g_var.set(g)

    a = await generate_a()
    a_var.set(a)

    g_a = pow(g, a, dh_prime)

    logger.debug(f'DH prime: {dh_prime}')
    logger.debug(f'g: {g}')
    logger.debug(f'a: {a}')
    logger.debug(f'g_a: {g_a}')

    server_dh_inner_data = Server_DH_inner_data(
        nonce=nonce,
        server_nonce=server_nonce,
        g=g,
        dh_prime=dump_integer_big_endian(dh_prime),
        g_a=dump_integer_big_endian(g_a),
        server_time=get_servertime()
    )

    server_dh_inner_bytes = dump_dh_inner_data(server_dh_inner_data)
    server_dh_prepared_data = prepare_for_encrypt(server_dh_inner_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce, inner_data.new_nonce)

    encrypted_server_dh = ige256_encrypt(
        server_dh_prepared_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    logger.info('Send dh params')
    return ServerDHParamsOk(
        nonce=nonce,
        server_nonce=server_nonce,
        encrypted_answer=encrypted_server_dh
    )
