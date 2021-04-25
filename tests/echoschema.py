# -*- coding: utf-8 -*-
import random
from dataclasses import dataclass

from aiohttp import web

from mtpylon import Schema


@dataclass
class Reply:
    rand_id: int
    content: str

    class Meta:
        name = 'reply'
        order = ('rand_id', 'content')


async def echo(request: web.Request, content: str) -> Reply:
    return Reply(
        rand_id=random.randint(1, 100),
        content=content
    )


schema = Schema(constructors=[Reply], functions=[echo])
