# -*- coding: utf-8 -*-
import pytest

from mtpylon.types import long
from mtpylon.crypto import AuthKey, AuthKeyManager
from mtpylon.contextvars import auth_key_var
from mtpylon.exceptions import (
    AuthKeyNotFound,
    AuthKeyChangedException,
)
from mtpylon.messages.encrypted_message import (
    unpack_message,
    Message
)
from mtpylon.serialization import CallableFunc
from mtpylon.utils import get_function_name

from tests.echoschema import schema

auth_key = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key_hash = 1394472671087208165269226426108057929670511175639
auth_key_id = 1435926575080417239

server_salt = long(16009147158398906513)
session_id = long(11520911270507767959)

encrypted_message_bytes = b"\x13\xedo\x9c\xb76'\xd7\xeaU\x0b\xba\xc0\xc4P\xad\x11\xdb\xcaB\x87\xff\xd4\xce\x83\x16\xbfbA\xbf1\xa7\x931\xe8.\x80\xe5\x1d\xb7$=\xc0\x98\x99O\x11\x8a\xb3\xb9P~\x1fb\x007\xab\xa7\x90\xa6\x0f\xa3\xa4\x9c<\xe2\x11u\xb4\xfc\xb6\x8b\x1cR\x96\xb7\xcf&\x01y:\xbf\xc3@\xc2\x9b\xe3E" # noqa


@pytest.mark.asyncio
async def test_unpack_message():
    auth_key_manager = AuthKeyManager()
    await auth_key_manager.set_key(auth_key)

    message = await unpack_message(
        auth_key_manager,
        schema,
        encrypted_message_bytes
    )

    assert isinstance(message, Message)
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
    await auth_key_manager.set_key(auth_key)

    current_auth_key = AuthKey(long(123123123))
    auth_key_var.set(current_auth_key)

    with pytest.raises(AuthKeyChangedException):
        await unpack_message(
            auth_key_manager,
            schema,
            encrypted_message_bytes
        )
