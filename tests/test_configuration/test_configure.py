# -*- coding: utf-8 -*-
import pytest
import rsa  # type: ignore
from aiohttp.web import Application

from mtpylon.configuration.configure import configure_app
from mtpylon.configuration.constants import (
    API_VIEW,
    SCHEMA_VIEW,
    PUB_KEYS_VIEW
)
from mtpylon.constants import RSA_MANAGER_RESOURCE_NAME, \
    AUTH_KEY_MANAGER_RESOURCE_NAME, DH_PRIME_GENERATOR_RESOURCE_NAME, \
    SERVER_SALT_MANAGER_RESOURCE_NAME, SESSION_SUBJECT_RESOURCE_NAME, \
    ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
from mtpylon.crypto import KeyPair
from tests.simpleschema import schema


@pytest.mark.asyncio
async def test_configure_app():
    (pubkey, privkey) = rsa.newkeys(1024)
    rsa_key_pair = KeyPair(
        private=privkey,
        public=pubkey
    )
    app = Application()

    configure_app(
        app,
        schema,
        {
            'rsa_manager': {
                'params': {
                    'rsa_keys': [
                        rsa_key_pair
                    ]
                }
            },
            'pub_keys_path': '/pub-keys',
            'schema_path': '/schema'
        }
    )

    assert RSA_MANAGER_RESOURCE_NAME in app
    assert AUTH_KEY_MANAGER_RESOURCE_NAME in app
    assert DH_PRIME_GENERATOR_RESOURCE_NAME in app
    assert SERVER_SALT_MANAGER_RESOURCE_NAME in app
    assert SESSION_SUBJECT_RESOURCE_NAME in app
    assert ACKNOWLEDGEMENT_STORE_RESOURCE_NAME in app

    assert API_VIEW in app.router
    assert SCHEMA_VIEW in app.router
    assert PUB_KEYS_VIEW in app.router
