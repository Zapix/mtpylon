# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock

import pytest
from tgcrypto import ige256_encrypt  # type: ignore

from mtpylon import long, int128, int256
from mtpylon.constants import (
    RSA_MANAGER_RESOURCE_NAME,
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    SERVER_SALT_MANAGER_RESOURCE_NAME,
)
from mtpylon.service_schema.functions import set_client_DH_params
from mtpylon.service_schema.functions.set_client_DH_params_func import (
    failed_auth_key,
    build_new_nonce_hash,
    decrypt_inner_data,
    build_salt,
)
from mtpylon.contextvars import (
    server_nonce_var,
    new_nonce_var,
    g_var,
    a_var,
    dh_prime_var
)
from mtpylon.utils import dump_integer_big_endian
from mtpylon.crypto import AuthKey, AuthKeyManager
from mtpylon.dh_prime_generators.single_prime import DH_PRIME
from mtpylon.service_schema import dump
from mtpylon.service_schema.constructors import (
    Client_DH_Inner_Data,
    DHGenOk,
    DHGenRetry,
    DHGenFail,
)
from mtpylon.service_schema.functions.req_DH_params_func import (
    prepare_for_encrypt
)
from mtpylon.service_schema.utils import generate_tmp_key_iv

from tests.simple_manager import manager

nonce_value = int128(88224628713810667588887952107997447839)
server_nonce_value = int128(235045274609009641577718790092619182246)
new_nonce_value = int256(27656883100497326063247081440413753296956262631784917691178051366501222503918)  # noqa

g_value = 3
a_value = 10607381476045138659429265705348440307625228218615399831425584185383413389695789014363987332658374582690499482994606718751755213965999439454253417488373631405171792902828547859725540679855820104449608382680798055278078479574064866242012271485024474232610876338028466071314589667559615323800282193789902492268370552683377619135044334657302807891270636368616968819993057671291889084088625666009775351268967434348365119144603903657150515815070203739707470016454363236440191670708243801685869454735549745237693917581545341899078812940353438164410364205294519167606000056959661373873672169515310959397725380118405694859139  # noqa
ga_value = pow(g_value, a_value, DH_PRIME)

b_value = 13793299033669999324334361062393501554903415436747812314533436967171793687327392161337525812179091233949378005237487910175430712779534950156248983099507157305564723151671444636718693113928535757052016253408792730142127440568424672784653291389878527262849495564373173366543318818472515898556399884373922371359502373425645399415766148866809501542901633475590601507951903278592754255533413474040323211035778774023188657813114295685121155226288490650713403497710026832624477409686808809193715340984341378716164072438115455129743175716811812332589399385729879976892205997421362659173001784169414140002800726486783087439769  # noqa
b2_value = 4809925943043779177259491514440650782426411249681173690373683346075227861853046869276528545588443376851732941272077714589137397002716097935323227907043659705741209743360624604249241374721788847285754204837795511079990275620426775746902933493121199592102452146745479127771201731522649424617925376810394433562977871660264389880846843337795893963632698001833016744625780800874883950443751305983398635679537502685993959784328120012744022626811575262800249662475225884432089869372550289500971338290271666782717554926428938548827408587880062036348832606971795181166736940275120354553670848564756283839544924862124327692962  # noqa

gb_value = pow(g_value, b_value, DH_PRIME)
gb2_value = pow(g_value, b2_value, DH_PRIME)
gab_value = pow(ga_value, b_value, DH_PRIME)
gab2_value = pow(ga_value, b2_value, DH_PRIME)
auth_key = AuthKey(gab_value)
auth_key2 = AuthKey(gab2_value)

new_nonce_hash1 = int128(297742614194472606733379134878680138370)
new_nonce_hash2 = int128(334754903444040789434393452372482067063)
new_nonce_hash3 = int128(98077897061349472903732881789191985947)


def setup_function(function):
    server_nonce_var.set(server_nonce_value)
    new_nonce_var.set(new_nonce_value)

    dh_prime_var.set(DH_PRIME)
    g_var.set(g_value)
    a_var.set(a_value)


@pytest.fixture
def aiohttp_request():
    """
    Returns mocked aiohttp request
    """
    request = MagicMock()
    server_salt_manager = MagicMock()
    server_salt_manager.set_salt = AsyncMock()

    request.app = {
        RSA_MANAGER_RESOURCE_NAME: manager,
        SERVER_SALT_MANAGER_RESOURCE_NAME: server_salt_manager
    }

    return request


def test_build_new_nonce_hash_1():
    assert build_new_nonce_hash(
        new_nonce_value,
        auth_key,
        1
    ) == new_nonce_hash1


def test_build_new_nonce_hash_2():
    assert build_new_nonce_hash(
        new_nonce_value,
        auth_key,
        2
    ) == new_nonce_hash2


def test_build_new_nonce_hash_3():
    assert build_new_nonce_hash(
        new_nonce_value,
        auth_key,
        3
    ) == new_nonce_hash3


def test_decrypt_correct_inner_data():
    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    decrypted_data = decrypt_inner_data(encrypted_data, key_iv_pair)

    assert decrypted_data == inner_data


def test_wrong_data_encrypted():
    inner_data_bytes = b'wrong_data_bytes'
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    with pytest.raises(ValueError):
        decrypt_inner_data(encrypted_data, key_iv_pair)


def test_wrong_hash():
    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = (
        (b'\x00' * 20) +
        prepare_for_encrypt(inner_data_bytes)[20:]
    )

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    with pytest.raises(ValueError):
        decrypt_inner_data(encrypted_data, key_iv_pair)


@pytest.mark.asyncio
async def test_set_client_dh_gen_ok(aiohttp_request):
    auth_key_manager = AuthKeyManager()
    aiohttp_request.app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager

    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    result = await set_client_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        encrypted_data
    )

    assert isinstance(result, DHGenOk)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value
    assert result.new_nonce_hash1 == new_nonce_hash1
    assert await auth_key_manager.has_key(auth_key)

    aiohttp_request.app[
        SERVER_SALT_MANAGER_RESOURCE_NAME
    ].set_salt.assert_awaited()


@pytest.mark.asyncio
async def test_set_client_dh_gen_retry(aiohttp_request):
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key)
    aiohttp_request.app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager

    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    result = await set_client_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        encrypted_data
    )

    assert isinstance(result, DHGenRetry)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value
    assert result.new_nonce_hash2 == new_nonce_hash2


@pytest.mark.asyncio
async def test_set_client_dh_gen_fail(aiohttp_request):
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key)
    aiohttp_request.app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager

    failed_auth_key.set(auth_key)

    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb2_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    result = await set_client_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        encrypted_data
    )

    assert isinstance(result, DHGenFail)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value
    assert result.new_nonce_hash3 == build_new_nonce_hash(
        new_nonce_value,
        auth_key2,
        3
    )


@pytest.mark.asyncio
async def test_set_cliend_dh_gen_ok_second_attempt(aiohttp_request):
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key)
    aiohttp_request.app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager

    failed_auth_key.set(auth_key)

    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(auth_key.aux_hash),
        g_b=dump_integer_big_endian(gb2_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    result = await set_client_DH_params(
        aiohttp_request,
        nonce_value,
        server_nonce_value,
        encrypted_data
    )

    assert isinstance(result, DHGenOk)
    assert result.nonce == nonce_value
    assert result.server_nonce == server_nonce_value
    assert result.new_nonce_hash1 == build_new_nonce_hash(
        new_nonce_value,
        auth_key2,
        1
    )

    aiohttp_request.app[
        SERVER_SALT_MANAGER_RESOURCE_NAME
    ].set_salt.assert_awaited()


@pytest.mark.asyncio
async def test_set_client_dh_wrong_server_nonce(aiohttp_request):
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key)
    aiohttp_request.app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager

    inner_data = Client_DH_Inner_Data(
        nonce=nonce_value,
        server_nonce=server_nonce_value,
        retry_id=long(0),
        g_b=dump_integer_big_endian(gb_value)
    )

    inner_data_bytes = dump(inner_data)
    prepared_inner_data = prepare_for_encrypt(inner_data_bytes)

    key_iv_pair = generate_tmp_key_iv(server_nonce_value, new_nonce_value)

    encrypted_data = ige256_encrypt(
        prepared_inner_data,
        key_iv_pair.key,
        key_iv_pair.iv
    )

    with pytest.raises(ValueError):
        await set_client_DH_params(
            aiohttp_request,
            nonce_value,
            int128(0),
            encrypted_data
        )


def test_build_server_salt():
    server_nonce1 = int128(249614136491309141700663873799696366784)
    new_nonce1 = int256(88757849913661402246725644620299906980168231292277558494010613000920485514672)  # noqa

    expected_salt = long(15255682115388961136)

    salt = build_salt(server_nonce1, new_nonce1)

    assert salt.salt == expected_salt
