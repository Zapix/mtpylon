# -*- coding: utf-8 -*-
import rsa  # type: ignore
from aiohttp.web import Application

from mtpylon.configuration.configure import configure
from mtpylon.configuration.constants import (
    RSA_MANAGER_RESOURCE_NAME,
)
from mtpylon.crypto import KeyPair
from tests.simpleschema import schema


def test_configure_app():
    (pubkey, privkey) = rsa.newkeys(1024)
    rsa_key_pair = KeyPair(
        private=privkey,
        public=pubkey
    )
    app = Application()

    configure(
        app,
        schema,
        {
            'rsa_manager': {
                'params': {
                    'rsa_keys': [
                        rsa_key_pair
                    ]
                }
            }
        }
    )

    assert RSA_MANAGER_RESOURCE_NAME in app
