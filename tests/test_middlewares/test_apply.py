# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock

import pytest

from mtpylon.middlewares import apply_middleware

from tests.simpleschema import set_task, Task


@pytest.mark.asyncio
async def test_apply_middleware():

    async def simple_middleware(handler, request, **params):
        return await handler(request, **params)

    middleware1 = AsyncMock(side_effect=simple_middleware)
    middleware2 = AsyncMock(side_effect=simple_middleware)

    handler = apply_middleware([middleware1, middleware2], set_task)

    request = MagicMock()

    result = await handler(request, content='hello world')

    assert isinstance(result, Task)
    assert result.content == 'hello world'

    middleware1.assert_awaited()
    middleware2.assert_awaited()
