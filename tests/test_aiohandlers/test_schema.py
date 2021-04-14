# -*- coding: utf-8 -*-
import pytest
from aiohttp.web import Application

from mtpylon.aiohandlers.schema import schema_view_factory

from tests.simpleschema import schema
from tests.test_serializers import json_schema


@pytest.fixture
def cli(loop, aiohttp_client):
    schema_view = schema_view_factory(schema)

    app = Application()
    app.router.add_get('/schema', schema_view)

    return loop.run_until_complete(aiohttp_client(app))


async def test_get_schema(cli):
    resp = await cli.get('/schema')

    assert resp.status == 200

    schema_data = await resp.json()

    assert schema_data == json_schema
