# -*- coding: utf-8 -*-
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from mtpylon.aiohandlers.webscockets import create_websocket_handler

from tests.simpleschema import schema


class WsHandlerTestCase(AioHTTPTestCase):

    async def get_application(self):
        ws_handler = create_websocket_handler(schema)

        app = web.Application()
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
        async with self.client.ws_connect('/ws') as conn:
            await conn.send_bytes(b'wrong bytes')
            await conn.receive()
            assert conn.closed

    @unittest_run_loop
    async def test_transport_tag_not_found(self):
        wrong_header = b'e023d49daf39cbca35a231c3aa284424157ad182c3c43ecfea30dcd94bf31ed197e595e249f616b95af94e5d1aef78bc556e5aa3c8cb1740b20b4d5f07436fcb'  # noqa
        async with self.client.ws_connect('/ws') as conn:
            await conn.send_bytes(wrong_header)
            await conn.receive()
            assert conn.closed

    @unittest_run_loop
    async def test_valid_transport_tag_passed(self):
        good_header = b'e023d49daf39cbca35a231c3aa284424157ad182c3c43ecfea30dcd94bf31ed197e595e249f616b95af94e5d1aef78bc556e5aa3c8cb1740b20b4d5f07436fcb'  # noqa
        async with self.client.ws_connect('/ws') as conn:
            await conn.send_bytes(good_header)
            assert not conn.closed
