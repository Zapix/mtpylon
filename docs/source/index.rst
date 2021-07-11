.. mtpylon documentation master file, created by
   sphinx-quickstart on Thu Oct 22 23:29:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mtpylon's documentation!
===================================

.. image:: https://github.com/Zapix/mtpylon/workflows/Running%20Tests/badge.svg
  :alt: Running Tests

.. image:: https://codecov.io/gh/Zapix/mtpylon/branch/dev/graph/badge.svg?token=4TWNMM7PCP
  :target: https://codecov.io/gh/Zapix/mtpylon
  :alt: codecov

Library to build backend with MTProto's protoco

.. _mtpylon_installation:

Installation
------------

.. code-block::

  pip install mtpylon

.. _mtpylon_getting_started:

Getting started
---------------

1. Generate rsa keys

**rsa_keys.py:**

.. code-block:: python

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

2. Declare schema for mtpylon

.. code-block:: python

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


3. Configure aiohttp with mtpylon

.. code-block:: python

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


4. Start it!

.. code-block::

  python web.py


5. to work with backend please try `<https://github.com/Zapix/zagram>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   0-basic-types
   1-combinators-and-constructors
   2-schema-and-its-serializers
   3-rsa-key-manager
   4-auth-key-and-auth-key-manager
   5-server-salt-manager
   6-session-subject-and-storage
   7-acknowledgement-store

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
