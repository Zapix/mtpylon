# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from mtpylon.types import long
from mtpylon.constants import SERVER_SALT_MANAGER_RESOURCE_NAME
from mtpylon.messages import EncryptedMessage
from mtpylon.serialization import CallableFunc
from mtpylon.middlewares.set_server_salt import set_server_salt
from mtpylon.crypto import AuthKey
from mtpylon.salts import ServerSaltManager, Salt
from mtpylon.contextvars import (
    income_message_var,
    auth_key_var,
    server_salt_var
)
from mtpylon.service_schema.constructors import BadServerSalt

from tests.simpleschema import set_task


@pytest.mark.asyncio
async def test_server_salt_exist():
    auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
    auth_key = AuthKey(auth_key_data)
    auth_key_var.set(auth_key)

    msg_id = long(0x51e57ac42770964a)
    session_id = long(123123)
    server_salt = Salt(
        salt=long(234234),
        since=datetime.now() - timedelta(hours=1),
        until=datetime.now() + timedelta(days=12),
    )

    message = EncryptedMessage(
        salt=server_salt.salt,
        session_id=session_id,
        message_id=msg_id,
        seq_no=1,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    income_message_var.set(message)

    server_salt_manager = ServerSaltManager()
    await server_salt_manager.set_salt(auth_key, server_salt)

    handler = AsyncMock()

    request = MagicMock()
    request.app = {
        SERVER_SALT_MANAGER_RESOURCE_NAME: server_salt_manager
    }

    await set_server_salt(handler, request, content='hello_world')

    handler.assert_awaited()
    assert server_salt_var.get() == server_salt.salt


@pytest.mark.asyncio
async def test_bad_server_salt():
    auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
    auth_key = AuthKey(auth_key_data)
    auth_key_var.set(auth_key)

    msg_id = long(0x51e57ac42770964a)
    session_id = long(123123)
    salt = long(234234)

    message = EncryptedMessage(
        salt=salt,
        session_id=session_id,
        message_id=msg_id,
        seq_no=1,
        message_data=CallableFunc(
            func=set_task,
            params={'content': 'hello world'}
        )
    )

    income_message_var.set(message)

    server_salt_manager = ServerSaltManager()

    handler = AsyncMock()

    request = MagicMock()
    request.app = {
        SERVER_SALT_MANAGER_RESOURCE_NAME: server_salt_manager
    }

    result = await set_server_salt(handler, request, content='hello_world')

    assert isinstance(result, BadServerSalt)
    assert result.error_code == 48
    assert result.bad_msg_id == msg_id
