# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from mtpylon import long
from mtpylon.constants import (
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
)
from mtpylon.message_sender import MessageSender
from mtpylon.crypto import AuthKeyManager, AuthKey
from mtpylon.contextvars import auth_key_var
from mtpylon.acknowledgement_store.types import AcknowledgementMessage
from mtpylon.messages import EncryptedMessage
from mtpylon.service_schema.constructors import MessageContainer

from tests.simpleschema import schema


auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key = AuthKey(auth_key_data)


@pytest.fixture
def aiohttp_request():
    request = MagicMock()
    request.app = {
        AUTH_KEY_MANAGER_RESOURCE_NAME: AuthKeyManager(),
        ACKNOWLEDGEMENT_STORE_RESOURCE_NAME: MagicMock(
            get_message_list=AsyncMock(return_value=[]),
            set_message=AsyncMock(),
        ),
    }

    return request


@pytest.mark.asyncio
async def test_send_unencrypted_message_ok(aiohttp_request):
    pack_message = AsyncMock(return_value=b'packed value')

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = False
        ws.send_bytes = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_unencrypted_message(
            aiohttp_request,
            'response_data',
            True
        )

        pack_message.assert_awaited()

        transport_wrapper.wrap.assert_called_with(b'packed value')
        obfuscator.encrypt.assert_called_with(b'wrapped value')

        ws.send_bytes.assert_awaited_with(b'encrypted value')


@pytest.mark.asyncio
async def test_send_encrypted_message_ok(aiohttp_request):
    auth_key_var.set(auth_key)

    pack_message = AsyncMock(return_value=b'packed value')

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = False
        ws.send_bytes = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_encrypted_message(
            aiohttp_request,
            long(234234),
            long(423422),
            'response_data',
            True
        )

        pack_message.assert_awaited()

        transport_wrapper.wrap.assert_called_with(b'packed value')
        obfuscator.encrypt.assert_called_with(b'wrapped value')

        ws.send_bytes.assert_awaited_with(b'encrypted value')


@pytest.mark.asyncio
async def test_send_encrypted_message_acknowledgement_required(
    aiohttp_request
):
    auth_key_var.set(auth_key)

    pack_message = AsyncMock(return_value=b'packed_value')
    server_salt = long(234234)
    session_id = long(423422)

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted_value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = False
        ws.send_bytes = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_encrypted_message(
            aiohttp_request,
            server_salt,
            session_id,
            'response_data',
            response=True,
            acknowledgement_required=True
        )

        acknowledgement_store = aiohttp_request.app[
            ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
        ]

        acknowledgement_store.set_message.assert_awaited()

        set_message_args = acknowledgement_store.set_message.await_args[0]
        assert set_message_args[1] == session_id
        assert set_message_args[3] == 'response_data'


@pytest.mark.asyncio
async def test_send_encrypted_message_in_container():
    aiohttp_request = MagicMock()
    aiohttp_request.app = {
        AUTH_KEY_MANAGER_RESOURCE_NAME: AuthKeyManager(),
        ACKNOWLEDGEMENT_STORE_RESOURCE_NAME: MagicMock(
            get_message_list=AsyncMock(return_value=[
                AcknowledgementMessage(
                    message_id=long(1),
                    data='first data'
                ),
                AcknowledgementMessage(
                    message_id=long(2),
                    data='second data'
                )
            ]),
            set_message=AsyncMock(),
        ),
    }

    auth_key_var.set(auth_key)

    server_salt = long(234234)
    session_id = long(423422)

    pack_message = AsyncMock(return_value=b'packed_value')

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = False
        ws.send_bytes = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_encrypted_message(
            aiohttp_request,
            server_salt,
            session_id,
            'response_data',
            response=True,
            acknowledgement_required=True
        )

        acknowledgement_store = aiohttp_request.app[
            ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
        ]
        acknowledgement_store.get_message_list.assert_awaited()

        pack_message.assert_awaited()
        args = pack_message.await_args[0]
        message = args[2]
        assert isinstance(message, EncryptedMessage)

        msg_container = message.message_data
        assert isinstance(msg_container, MessageContainer)

        assert len(msg_container.messages) == 3


@pytest.mark.asyncio
async def test_send_message_value_error(aiohttp_request):
    auth_key_var.set(auth_key)

    pack_message = AsyncMock(side_effect=ValueError('error durig pack'))

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = False
        ws.close = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_unencrypted_message(
            aiohttp_request,
            'response_data',
            True
        )

        pack_message.assert_awaited()

        ws.close.assert_awaited()


@pytest.mark.asyncio
async def test_send_message_ws_closed(aiohttp_request):
    auth_key_var.set(auth_key)

    pack_message = AsyncMock(return_value=b'packed value')

    with patch('mtpylon.message_sender.pack_message', pack_message):
        obfuscator = MagicMock()
        obfuscator.encrypt.return_value = b'encrypted value'

        transport_wrapper = MagicMock()
        transport_wrapper.wrap.return_value = b'wrapped value'

        ws = MagicMock()
        ws.closed = True
        ws.close = AsyncMock()
        ws.send_bytes = AsyncMock()

        sender = MessageSender(
            schema=schema,
            obfuscator=obfuscator,
            transport_wrapper=transport_wrapper,
            ws=ws
        )

        await sender.send_unencrypted_message(
            aiohttp_request,
            'response_data',
            True
        )

        ws.close.assert_not_awaited()
        ws.send_bytes.assert_not_awaited()

        obfuscator.ecnrypt.assert_not_called()
        transport_wrapper.wrap.assert_not_called()
        pack_message.assert_not_awaited()
