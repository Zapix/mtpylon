# -*- coding: utf-8 -*-
from functools import partial

from aiohttp.web import Request, Response
from aiohttp.web_response import json_response

from .types import RequestHandler
from ..schema import Schema
from ..serializers import to_dict


async def schema_view(request: Request, schema: Schema) -> Response:
    """
    Returns schema as dumped json
    """
    return json_response(
        to_dict(schema),
        status=200,
    )


def schema_view_factory(schema: Schema) -> RequestHandler:
    return partial(schema_view, schema=schema)
