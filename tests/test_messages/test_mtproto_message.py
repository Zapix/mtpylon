# -*- coding: utf-8 -*-
import pytest
from tgcrypto import ige256_decrypt  # type: ignore

from mtpylon import long, int128
from mtpylon.messages import (
    EncryptedMessage,
    UnencryptedMessage,
    pack_message,
    unpack_message,
)
from mtpylon.crypto import (
    AuthKeyManager,
    AuthKey,
    generate_key_iv,
)
from mtpylon.messages.encrypted_message import load_message
from mtpylon.service_schema.functions import req_pq
from mtpylon.service_schema.constructors import ResPQ
from mtpylon.serialization.schema import CallableFunc
from mtpylon.utils import get_function_name
from mtpylon.serialization.int128 import load as load_int128
from mtpylon.contextvars import auth_key_var

from tests.echoschema import schema, Reply


auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key_hash = 1394472671087208165269226426108057929670511175639
auth_key_id = 1435926575080417239

server_salt = long(16009147158398906513)
session_id = long(11520911270507767959)

encrypted_message_bytes = b"\x13\xedo\x9c\xb76'\xd7\xeaU\x0b\xba\xc0\xc4P\xad\x11\xdb\xcaB\x87\xff\xd4\xce\x83\x16\xbfbA\xbf1\xa7\x931\xe8.\x80\xe5\x1d\xb7$=\xc0\x98\x99O\x11\x8a\xb3\xb9P~\x1fb\x007\xab\xa7\x90\xa6\x0f\xa3\xa4\x9c<\xe2\x11u\xb4\xfc\xb6\x8b\x1cR\x96\xb7\xcf&\x01y:\xbf\xc3@\xc2\x9b\xe3E" # noqa

encoded_req_pq_message = (
    b'\x00\x00\x00\x00\x00\x00\x00\x00' +
    b'\x4a\x96\x70\x27\xc4\x7a\xe5\x51' +
    b'\x14\x00\x00\x00' +
    b'\x78\x97\x46\x60' +
    b'\x3e\x05\x49\x82\x8c\xca\x27\xe9\x66\xb3\x01\xa4\x8f\xec\xe2\xfc'
)

req_pq_message = UnencryptedMessage(
    message_id=long(0x51e57ac42770964a),
    message_data=CallableFunc(
        func=req_pq,
        params={
            'nonce': int128(0xfce2ec8fa401b366e927ca8c8249053e),
        },
    ),
)

encoded_res_pq = (
    b'\x00\x00\x00\x00\x00\x00\x00\x00' +
    b'\x01\x84\x67\xb9\xf4\x1d\x42\x60' +
    b'\x40\x00\x00\x00' +
    b'\x63\x24\x16\x05' +
    b'\xb4\xbd\x9d\x5f\xd2\x98\x4f\x16\x04\x14\x4e\x16\x77\xd7\xce\x88' +
    b'\x35\x5b\xea\x59\x40\xcc\x59\x3e\x7e\xc4\xc0\xbf\xc1\x23\x3d\x86' +
    b'\x08\x13\x54\x65\x62\x4e\x61\x25\xfd\x00\x00\x00' +
    b'\x15\xc4\xb5\x1c' +
    b'\x01\x00\x00\x00' +
    b'\x21\x6b\xe8\x6c\x02\x2b\xb4\xc3'
)

res_pq_message = UnencryptedMessage(
    message_id=long(0x60421df4b9678401),
    message_data=ResPQ(
        nonce=int128(0x88ced777164e1404164f98d25f9dbdb4),
        server_nonce=int128(0x863d23c1bfc0c47e3e59cc4059ea5b35),
        pq=b'\x13\x54\x65\x62\x4e\x61\x25\xfd',
        server_public_key_fingerprints=[
            long(0xc3b42b026ce86b21),
        ],
    ),
)


message_tests = [
    pytest.param(
        encoded_req_pq_message,
        req_pq_message,
        id='req_pq'
    ),
    pytest.param(
        encoded_res_pq,
        res_pq_message,
        id='ResPQ'
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'encoded_message,expected_message',
    message_tests
)
async def test_unpack_unencrypted(encoded_message, expected_message):
    auth_key_manager = AuthKeyManager()
    message = await unpack_message(
        auth_key_manager,
        schema,
        encoded_message
    )

    assert message == expected_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'encoded_message,message',
    message_tests
)
async def test_pack_unencrypted(encoded_message, message):
    auth_key_manager = AuthKeyManager()
    encoded = await pack_message(
        auth_key_manager,
        schema,
        message
    )

    assert encoded == encoded_message


@pytest.mark.asyncio
async def test_unpack_message():
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key_data)

    message = await unpack_message(
        auth_key_manager,
        schema,
        encrypted_message_bytes
    )

    assert isinstance(message, EncryptedMessage)
    assert message.salt == server_salt

    assert message.session_id == session_id

    assert isinstance(message.message_data, CallableFunc)

    func = message.message_data.func
    params = message.message_data.params

    assert get_function_name(func) == 'echo'
    assert 'content' in params
    assert params['content'] == 'hello world'


@pytest.mark.asyncio
async def test_pack_message():
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key_data)

    auth_key = AuthKey(auth_key_data)
    auth_key_var.set(auth_key)

    value = Reply(
        rand_id=83,
        content='hello world'
    )

    message = EncryptedMessage(
        salt=server_salt,
        session_id=session_id,
        message_id=long(0),
        seq_no=0,
        message_data=value
    )

    dumped_message = await pack_message(auth_key_manager, schema, message)

    assert int.from_bytes(dumped_message[:8], 'big') == auth_key_id

    msg_key_bytes = dumped_message[8:24]
    msg_key = load_int128(msg_key_bytes).value

    key_iv_pair = generate_key_iv(auth_key, msg_key)

    original_data_bytes = ige256_decrypt(
        dumped_message[24:],
        key_iv_pair.key,
        key_iv_pair.iv
    )

    loaded_data = await load_message(schema, original_data_bytes)

    assert loaded_data == message
