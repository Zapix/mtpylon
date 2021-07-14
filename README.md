# mtpylon


![Running Tests](https://github.com/Zapix/mtpylon/workflows/Running%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/Zapix/mtpylon/branch/dev/graph/badge.svg?token=4TWNMM7PCP)](https://codecov.io/gh/Zapix/mtpylon)

Library to build backend with MTProto's protocol

## Installation

```shell
pip install mtpylon
```

## Getting started

1. Generate rsa keys:

**rsa_keys.py:**

```python
from typing import List
import rsa  # type: ignore
from mtpylon.crypto import KeyPair  # type: ignore


def get_rsa_keys(count: int = 2) -> List[KeyPair]:
    rsa_list = [
        rsa.newkeys(nbits=2048)
        for _ in range(count)
    ]

    return [
        KeyPair(
            public=public,
            private=private
        ) for (public, private) in rsa_list
    ]
```


2. Declare schema for mtpylon

**schema.py:**

```python
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

```

3. Configure aiohttp with mtpylon

**web.py:**
```python
import sys
import logging

from aiohttp import web
import aiohttp_cors

from mtpylon.configuration import configure_app

from schema import schema as app_schema
from rsa_keys import get_rsa_keys

# create console handler and set level to debug
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(level=logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    app = web.Application()
    configure_app(
        app,
        app_schema,
        {
            'rsa_manager': {
                'params': {
                    'rsa_keys': get_rsa_keys()
                }
            },
            'pub_keys_path': '/pub-keys',
            'schema_path': '/schema',
        }
    )

    cors = aiohttp_cors.setup(
        app,
        defaults={
            '*': aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        }
    )

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, port=8081)

```

4. Start it!

```shell
python web.py
```

5. to work with backend please try https://github.com/Zapix/zagram

## Documentation

For more information visit:

https://mtpylon.readthedocs.io/en/latest/

## Example:

Echo server: https://github.com/Zapix/echo-server
