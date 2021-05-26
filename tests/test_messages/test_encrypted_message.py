# -*- coding: utf-8 -*-
import pytest
from tgcrypto import ige256_decrypt  # type: ignore

from mtpylon.types import long
from mtpylon.crypto import (
    AuthKey,
    AuthKeyManager,
    generate_key_iv
)
from mtpylon.exceptions import DumpError
from mtpylon.contextvars import auth_key_var
from mtpylon.exceptions import (
    AuthKeyNotFound,
    AuthKeyChangedException,
)
from mtpylon.messages.encrypted_message import (
    unpack_message,
    load_data,
    dump_data,
    pack_message,
    load_message
)
from mtpylon.messages import EncryptedMessage
from mtpylon.serialization import CallableFunc
from mtpylon.serialization.int128 import load as load_int128
from mtpylon.utils import get_function_name

from tests.echoschema import schema, Reply

auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key_hash = 1394472671087208165269226426108057929670511175639
auth_key_id = 1435926575080417239

server_salt = long(16009147158398906513)
session_id = long(11520911270507767959)

encrypted_message_bytes = b"\x13\xedo\x9c\xb76'\xd7\xeaU\x0b\xba\xc0\xc4P\xad\x11\xdb\xcaB\x87\xff\xd4\xce\x83\x16\xbfbA\xbf1\xa7\x931\xe8.\x80\xe5\x1d\xb7$=\xc0\x98\x99O\x11\x8a\xb3\xb9P~\x1fb\x007\xab\xa7\x90\xa6\x0f\xa3\xa4\x9c<\xe2\x11u\xb4\xfc\xb6\x8b\x1cR\x96\xb7\xcf&\x01y:\xbf\xc3@\xc2\x9b\xe3E" # noqa


def test_dump_data_success():
    reply = Reply(
        content='hello world',
        rand_id=44,
    )

    reply_bytes = (
        b'>\x00j\r,\x00\x00\x00\x0bhello world'
    )

    assert dump_data(schema, reply) == reply_bytes


def test_dump_data_error():
    with pytest.raises(DumpError):
        dump_data(schema, 'fake data')


def test_load_success():
    reply_bytes = (
        b'>\x00j\r,\x00\x00\x00\x0bhello world'
    )

    value = load_data(schema, reply_bytes)

    assert isinstance(value, Reply)


def test_load_data_error():
    with pytest.raises(ValueError):
        load_data(schema, b'fakedata')


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
async def test_unpack_message_auth_key_not_found():
    auth_key_manager = AuthKeyManager()

    with pytest.raises(AuthKeyNotFound):
        await unpack_message(
            auth_key_manager,
            schema,
            encrypted_message_bytes
        )


@pytest.mark.asyncio
async def test_unpack_message_ohter_auth_key():
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key_data)

    current_auth_key = AuthKey(long(123123123))
    auth_key_var.set(current_auth_key)

    with pytest.raises(AuthKeyChangedException):
        await unpack_message(
            auth_key_manager,
            schema,
            encrypted_message_bytes
        )


@pytest.mark.asyncio
async def test_pack_message():
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

    dumped_message = await pack_message(schema, message)

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


@pytest.mark.asyncio
async def test_pack_message_auth_key_not_set():
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

    with pytest.raises(ValueError):
        await pack_message(schema, message)
