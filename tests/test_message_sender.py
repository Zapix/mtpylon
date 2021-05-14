# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from mtpylon import long
from mtpylon.message_sender import MessageSender
from mtpylon.crypto import AuthKeyManager

from tests.simpleschema import schema


@pytest.fixture
def aiohttp_request():
    request = MagicMock()
    request.app = {
        'auth_key_manager': AuthKeyManager(),
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
async def test_send_message_value_error(aiohttp_request):
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
