# -*- coding: utf-8 -*-
import pytest
from aiohttp.web import Application

from mtpylon.aiohandlers.pub_keys import pub_keys_view

from tests.simple_manager import manager


@pytest.fixture
def cli(loop, aiohttp_client):

    app = Application()
    app.router.add_get('/pub-keys', pub_keys_view)

    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def cli_with_manager(loop, aiohttp_client):

    app = Application()
    app['rsa_manager'] = manager
    app.router.add_get('/pub-keys', pub_keys_view)

    return loop.run_until_complete(aiohttp_client(app))


async def test_400_no_keys(cli):
    resp = await cli.get('/pub-keys')

    assert resp.status == 400


async def test_200_ok(cli_with_manager):

    resp = await cli_with_manager.get('/pub-keys')

    assert resp.status == 200
