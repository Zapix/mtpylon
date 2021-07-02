# -*- coding: utf-8 -*-
from contextlib import ExitStack
from unittest.mock import AsyncMock, MagicMock, patch

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from mtpylon.aiohandlers.websockets import create_websocket_handler
from mtpylon.crypto import AuthKeyManager
from mtpylon.dh_prime_generators.single_prime import generate
from mtpylon.salts import ServerSaltManager
from mtpylon.sessions import SessionSubject, InMemorySessionStorage
from mtpylon.acknowledgement_store import InmemoryAcknowledgementStore
from mtpylon.constants import (
    RSA_MANAGER_RESOURCE_NAME,
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    DH_PRIME_GENERATOR_RESOURCE_NAME,
    SERVER_SALT_MANAGER_RESOURCE_NAME,
    SESSION_SUBJECT_RESOURCE_NAME,
    ACKNOWLEDGEMENT_STORE_RESOURCE_NAME,
)

from tests.helpers import hexstr_to_bytes
from tests.simple_manager import manager
from tests.simpleschema import schema


wrong_header = hexstr_to_bytes(
    'e023d49daf39cbca35a231c3aa284424157ad182c3c43ecfea30dcd94bf31ed197e595e249f616b95af94e5d1aef78bc556e5aa3c8cb1740b20b4d5f07436fcb'  # noqa
)

good_header = hexstr_to_bytes(
    'ac12ac1df7f68e2eacd4085138d294d7f9d71000469b9fbdc6cf0cbb50382a5d34a38c29ae4e14945dded705a65625e02e206e7a12f9e13a6bdb572fe929ec85'  # noqa
)

clients_message = hexstr_to_bytes(
    'e7dbc655fbf3234c5f265c50c06482bd55ac73a906fdfee24b946ea3d268e42e11a1fccac23884200ffb7e67'  # noqa
)


class WsHandlerNoRsaManagerTestCase(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_rsa_manager(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerNoAuthkKeyManagerTestCase(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_auth_key_manager(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerNoDhPrimeGeneratorTestCase(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app[AUTH_KEY_MANAGER_RESOURCE_NAME] = AuthKeyManager()
        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_auth_key_manager(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerNoServerSaltManager(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app[AUTH_KEY_MANAGER_RESOURCE_NAME] = AuthKeyManager()
        app[DH_PRIME_GENERATOR_RESOURCE_NAME] = generate()

        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_server_salt_manager(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerNoSessionSubject(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app[AUTH_KEY_MANAGER_RESOURCE_NAME] = AuthKeyManager()
        app[DH_PRIME_GENERATOR_RESOURCE_NAME] = generate()
        app[SERVER_SALT_MANAGER_RESOURCE_NAME] = ServerSaltManager()

        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_session_subject(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerNoAcknowledgementStore(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app[AUTH_KEY_MANAGER_RESOURCE_NAME] = AuthKeyManager()
        app[DH_PRIME_GENERATOR_RESOURCE_NAME] = generate()
        app[SERVER_SALT_MANAGER_RESOURCE_NAME] = ServerSaltManager()
        app[SESSION_SUBJECT_RESOURCE_NAME] = SessionSubject(
            lambda: InMemorySessionStorage()
        )
        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_no_acknowledgement_store(self):
        logger = MagicMock()

        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                assert logger.error.called

            assert conn.closed


class WsHandlerTestCase(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
        app[RSA_MANAGER_RESOURCE_NAME] = manager
        app[AUTH_KEY_MANAGER_RESOURCE_NAME] = AuthKeyManager()
        app[DH_PRIME_GENERATOR_RESOURCE_NAME] = generate()
        app[SERVER_SALT_MANAGER_RESOURCE_NAME] = ServerSaltManager()
        app[SESSION_SUBJECT_RESOURCE_NAME] = SessionSubject(
            lambda: InMemorySessionStorage()
        )
        app[
            ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
        ] = InmemoryAcknowledgementStore()
        app.router.add_get('/ws', ws_handler)

        return app

    @unittest_run_loop
    async def test_connection(self):
        async with self.client.ws_connect('/ws') as conn:
            assert not conn.closed

        assert conn.closed

    @unittest_run_loop
    async def test_wrong_data_sent(self):
        async with self.client.ws_connect('/ws') as conn:
            await conn.send_str('Hello World')
            await conn.receive()
            assert conn.closed

    @unittest_run_loop
    async def test_can_not_properly_get_obfuscator(self):
        logger = MagicMock()
        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                await conn.send_bytes(b'wrong bytes')
                await conn.receive()
                assert conn.closed

        assert logger.error.called

    @unittest_run_loop
    async def test_transport_tag_not_found(self):
        logger = MagicMock()
        with patch('mtpylon.aiohandlers.websockets.logger', logger):
            async with self.client.ws_connect('/ws') as conn:
                await conn.send_bytes(wrong_header)
                await conn.receive()
                assert conn.closed

        assert logger.error.called

    @unittest_run_loop
    async def test_valid_transport_tag_passed(self):
        logger = MagicMock()
        MessageHandler = MagicMock()
        with ExitStack() as patcher:
            patcher.enter_context(
                patch(
                    'mtpylon.aiohandlers.websockets.logger',
                    logger
                )
            )
            patcher.enter_context(
                patch(
                    'mtpylon.aiohandlers.websockets.MessageHandler',
                    MessageHandler
                )
            )
            async with self.client.ws_connect('/ws') as conn:
                await conn.send_bytes(good_header)
                assert not conn.closed

        assert not logger.error.called, logger.error.call_args[0]
        assert MessageHandler.called

    @unittest_run_loop
    async def test_valid_transport_tag_message(self):
        logger = MagicMock()

        message_entity = AsyncMock()
        MessageHandler = MagicMock(return_value=message_entity)
        MessageSender = MagicMock()

        with ExitStack() as patcher:
            patcher.enter_context(
                patch(
                    'mtpylon.aiohandlers.websockets.logger',
                    logger
                )
            )
            patcher.enter_context(
                patch(
                    'mtpylon.aiohandlers.websockets.MessageHandler',
                    MessageHandler
                )
            )
            patcher.enter_context(
                patch(
                    'mtpylon.aiohandlers.websockets.MessageSender',
                    MessageSender
                )
            )
            async with self.client.ws_connect('/ws') as conn:
                await conn.send_bytes(good_header)
                await conn.send_bytes(clients_message)
                assert not conn.closed

        assert not logger.error.called, logger.error.call_args[0]
        assert MessageHandler.called
        assert MessageSender.called
        assert message_entity.handle.called
