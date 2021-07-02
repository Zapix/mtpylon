# -*- coding: utf-8 -*-
import logging
from typing import cast, Literal, Optional
from hashlib import sha1
from contextvars import ContextVar

from aiohttp import web
from tgcrypto import ige256_decrypt  # type: ignore

from mtpylon import Schema, long, int128, int256
from mtpylon.constants import (
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    SERVER_SALT_MANAGER_RESOURCE_NAME
)
from mtpylon.crypto import AuthKey, KeyIvPair
from mtpylon.crypto.auth_key_manager import AuthKeyManagerProtocol
from mtpylon.salts import ServerSaltManagerProtocol
from mtpylon.contextvars import (
    new_nonce_var,
    server_nonce_var,

    a_var,
    dh_prime_var,
)
from mtpylon.serialization import LoadedValue
from mtpylon.serialization.schema import load
from mtpylon.serialization.int256 import (
    dump as dump_int256
)
from mtpylon.serialization.int128 import (
    load as load_int128,
    dump as dump_int128
)
from mtpylon.salts import Salt
from ..utils import generate_tmp_key_iv
from ..constructors import (
    Set_client_DH_params_answer,
    DHGenOk,
    DHGenFail,
    DHGenRetry,
    Client_DH_Inner_Data
)


logger = logging.getLogger('mtpylon.authorization')


HASH_MODE = Literal[1, 2, 3]


failed_auth_key: ContextVar[Optional[AuthKey]] = ContextVar(
    'failed_auth_key',
    default=None
)


def build_new_nonce_hash(
    new_nonce: int256,
    auth_key: AuthKey,
    hash_type: HASH_MODE
) -> int128:
    """
    new_nonce_hash1, new_nonce_hash2, and new_nonce_hash3 are obtained as
    the 128 lower-order bits of SHA1 of the byte string derived from
    the new_nonce string by adding a single byte with the value of 1, 2, or 3,
    and followed by another 8 bytes with auth_key_aux_hash.
    Different values are required to prevent an intruder from changing server
    response dh_gen_ok into dh_gen_retry.
    """
    data = (
        dump_int256(new_nonce) +
        hash_type.to_bytes(1, 'big') +
        auth_key.aux_hash.to_bytes(8, 'big')
    )

    return load_int128(sha1(data).digest()[-16:]).value


def build_salt(server_nonce: int128, new_nonce: int256) -> Salt:
    """
    Builds new salt from server_nonce and new_nonces
    """
    server_nonce_bytes = dump_int128(server_nonce)
    new_nonce_bytes = dump_int256(new_nonce)

    salt_value = (
        int.from_bytes(server_nonce_bytes[:8], 'little') ^
        int.from_bytes(new_nonce_bytes[:8], 'little')
    )

    return Salt(salt=long(salt_value))


def load_client_dh_inner_data(
    raw_data: bytes
) -> LoadedValue[Client_DH_Inner_Data]:
    tmp_schema = Schema(
        constructors=[Client_DH_Inner_Data],
        functions=[]
    )
    loaded_value = load(raw_data, schema=tmp_schema)
    value = loaded_value.value

    value = cast(Client_DH_Inner_Data, loaded_value.value)

    return LoadedValue(value=value, offset=loaded_value.offset)


def decrypt_inner_data(
    encrypted_data: bytes,
    key_iv_pair: KeyIvPair
) -> Client_DH_Inner_Data:
    """
    Decrypts data with Client DH Inner data params.
    Checks that correct data loaded. Checks sha1 hash of decrypted data

    Raises:
        ValueError - if can't load data or hashes are not equals
    """
    decrypted_data = ige256_decrypt(
        encrypted_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    loaded_value = load_client_dh_inner_data(decrypted_data[20:])

    hash_data = decrypted_data[:20]

    if hash_data != sha1(decrypted_data[20:20 + loaded_value.offset]).digest():
        raise ValueError('Hashes are not equals')

    return loaded_value.value


async def set_client_DH_params(
    request: web.Request,
    nonce: int128,
    server_nonce: int128,
    encrypted_data: bytes
) -> Set_client_DH_params_answer:
    """
    Takes cliend encoded g_b value. Computes auth_key and checks can we set it
    to manager or not.o

    Raises:
        ValueError - if server nonce are not equals or can't correct decrypt
                     inner data

    Returns:
        DHGenOk - if key exchange successfully completes
        DHGenRetry - retry if key created but auth_key id has been used
        DHGenFail - wrong retry_id has been passed
    """
    logger.info("Handle set client dh params")
    server_nonce_value = server_nonce_var.get()
    new_nonce_value = new_nonce_var.get()
    logger.debug(f'server nonce: {server_nonce_value}')
    logger.debug(f'new nonce: {new_nonce_value}')

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    inner_data = decrypt_inner_data(encrypted_data, key_iv_pair)

    if (
        server_nonce != server_nonce_value or
        inner_data.server_nonce != server_nonce_value
    ):
        logger.error('Server nonce are not equals')
        raise ValueError('Server nonce are not equals')

    g_b = int.from_bytes(inner_data.g_b, 'big')
    a_value = a_var.get()
    dh_prime = dh_prime_var.get()
    gab_value = pow(g_b, a_value, dh_prime)

    auth_key = AuthKey(gab_value)

    failed_key = failed_auth_key.get(None)

    if (
        failed_key is not None and
        long(failed_key.aux_hash) != inner_data.retry_id
    ):
        return DHGenFail(
            nonce=nonce,
            server_nonce=server_nonce,
            new_nonce_hash3=build_new_nonce_hash(
                new_nonce_value,
                auth_key,
                3
            )
        )

    auth_manager = request.app[AUTH_KEY_MANAGER_RESOURCE_NAME]
    auth_manager = cast(AuthKeyManagerProtocol, auth_manager)

    if await auth_manager.has_key(auth_key):
        return DHGenRetry(
            nonce=nonce,
            server_nonce=server_nonce,
            new_nonce_hash2=build_new_nonce_hash(
                new_nonce_value,
                auth_key,
                2
            )
        )

    await auth_manager.set_key(auth_key)

    salt = build_salt(server_nonce, new_nonce_value)

    server_salt_manager = request.app[SERVER_SALT_MANAGER_RESOURCE_NAME]
    server_salt_manager = cast(ServerSaltManagerProtocol, server_salt_manager)

    await server_salt_manager.set_salt(auth_key, salt)

    logger.info('Auth key has been created:')
    logger.info(f'Auth key: {auth_key.value}')
    logger.info(f'Autk key hash: {auth_key.hash}')
    logger.info(f'Auth key id: {auth_key.id}')
    logger.info(f'Auth key aux hash: {auth_key.aux_hash}')
    logger.info(f'Server salt: {salt.salt}')

    return DHGenOk(
        nonce=nonce,
        server_nonce=server_nonce,
        new_nonce_hash1=build_new_nonce_hash(
            new_nonce_value,
            auth_key,
            1
        )
    )
