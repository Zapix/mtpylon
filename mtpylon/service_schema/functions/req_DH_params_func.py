# -*- coding: utf-8 -*-
import logging
from typing import cast
from hashlib import sha1
from datetime import datetime
from random import getrandbits

import rsa  # type: ignore
from tgcrypto import ige256_encrypt  # type: ignore

from mtpylon import Schema
from mtpylon.contextvars import (
    rsa_manager,
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
from mtpylon.crypto import KeyIvPair

from ..constructors import (
    Server_DH_Params,
    ServerDHParamsOk,
    ServerDHParamsFail,
    Server_DH_inner_data,
    P_Q_inner_data
)
from ...utils import int128, int256, long, dump_integer_big_endian
from ..utils import generate_a, generate_g, generate_dh_prime


logger = logging.getLogger('authorization_process')


def get_servertime():
    return int(datetime.now().timestamp())


def load_pq_inner_data(raw_data: bytes) -> LoadedValue[P_Q_inner_data]:
    tmp_schema = Schema(constructors=[P_Q_inner_data], functions=[])
    loaded_data = load(tmp_schema, raw_data)
    value = loaded_data.value

    value = cast(P_Q_inner_data, value)
    return LoadedValue(value=value, offset=loaded_data.offset)


def dump_dh_inner_data(data: Server_DH_inner_data):
    tmp_schema = Schema(constructors=[Server_DH_inner_data], functions=[])
    return dump(tmp_schema, data, custom_dumpers=None)


def decrypt_inner_data(
        encrypted_data: bytes,
        fingerprint: long
) -> P_Q_inner_data:
    manager = rsa_manager.get()

    if fingerprint not in manager:
        raise ValueError(f'Fingerprint {fingerprint} not found in manager')

    key_pair = manager[fingerprint]

    try:
        unencrypted_data = rsa.decrypt(encrypted_data, key_pair.private)
    except rsa.DecryptionError:
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


def generate_tmp_key_iv(server_nonce: int128, new_nonce: int256) -> KeyIvPair:
    server_nonce_bytes = dump_integer_big_endian(server_nonce)
    new_nonce_bytes = dump_integer_big_endian(new_nonce)
    new_server_hash = sha1(new_nonce_bytes + server_nonce_bytes).digest()
    server_new_hash = sha1(server_nonce_bytes + new_nonce_bytes).digest()

    key = new_server_hash + server_new_hash[:12]
    iv = server_new_hash[12:] + new_server_hash + new_nonce_bytes[:4]

    return KeyIvPair(key=key, iv=iv)


def prepare_for_encrypt(data: bytes) -> bytes:
    postfix_size = (16 - (len(data) + 20) % 16) % 16

    return (
        sha1(data).digest() +
        data +
        getrandbits(postfix_size).to_bytes(postfix_size, 'big')
    )


async def req_DH_params(
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
    inner_data = decrypt_inner_data(encrypted_data, public_key_fingerprint)
    new_nonce_var.set(inner_data.new_nonce)
    new_nonce_hash = build_new_nonce_hash(inner_data.new_nonce)

    if (
            server_nonce != server_nonce_var.get() or
            server_nonce != inner_data.server_nonce
    ):
        raise ValueError('Wrong server nonces')

    if not is_valid_pq_params(p, q, inner_data):
        logger.debug('Wrong server  pq params')
        return ServerDHParamsFail(
            nonce=nonce,
            server_nonce=server_nonce_var.get(),
            new_nonce_hash=new_nonce_hash
        )

    dh_prime = await generate_dh_prime()
    dh_prime_var.set(dh_prime)

    g = await generate_g()
    g_var.set(g)

    a = await generate_a()
    a_var.set(a)

    g_a = pow(g, a, dh_prime)

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

    return ServerDHParamsOk(
        nonce=nonce,
        server_nonce=server_nonce,
        encrypted_answer=encrypted_server_dh
    )
