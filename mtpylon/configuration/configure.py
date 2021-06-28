# -*- coding: utf-8 -*-
from aiohttp.web import Application

from mtpylon.schema import Schema
from .types import ConfigDict, RsaManagerDict, AuthKeyManagerDict
from .import_path import import_path
from .constants import (
    RSA_MANAGER_RESOURCE_NAME,
    DEFAULT_RSA_MANAGER_PATH,
    AUTH_KEY_MANAGER_RESOURCE_NAME,
    DEFAULT_AUTH_KEY_MANAGER_PATH
)


def configure_rsa_manager(app: Application, config: RsaManagerDict):
    """
    Configure rsa manager with dict config
    """
    rsa_manager_path = config.get('manager', DEFAULT_RSA_MANAGER_PATH)
    rsa_manager_class = import_path(rsa_manager_path)

    params = config.get('params', {})

    app[RSA_MANAGER_RESOURCE_NAME] = rsa_manager_class(**params)


def configure_auth_manager(app: Application, config: AuthKeyManagerDict):
    """
    Configure rsa manager with dict config
    """
    auth_key_manager_path = config.get(
        'manager',
        DEFAULT_AUTH_KEY_MANAGER_PATH
    )
    auth_key_manager_class = import_path(auth_key_manager_path)

    params = config.get('params', {})

    app[AUTH_KEY_MANAGER_RESOURCE_NAME] = auth_key_manager_class(**params)


def configure(
    app: Application,
    schema: Schema,
    config: ConfigDict
):
    """
    Configure aiohttp Application to handle mtpylon protocol.
    Customer could configure several parts of mtpylon. Each part
    has got it's own key value in config dictionary.

     * `rsa_manager` - manager to store private and public keys of your
    application.

     * `auth_key_manager` - stores info about registered auth keys

     * `server_salt_manager` - manager of server salt that require for
     client server message exchange and prevents against replay attack

     * `session_storage` - storage for storing session_ids.

     * `acknowledgement_storage`' - storage of messages that hasn't received
     acknowledgement

    Customer could configure main views for this schema:

     * `pub_keys_view` - if set then `mtpylon.aiohandlers.pub_keys_view` will
     be include to asyncio app. by uri that you pass as value of this params

     * `schema_view` - if set then creates view with
     `mtpylon.aiohandlers.schema_view_factory` and include to asyncio app.
     Uri to include is passed as value of this param

     * `api_view` - add main view by uri that passed in this param or use `/ws`
     as default
    """
    configure_rsa_manager(app, config.get('rsa_manager', {}))
    configure_auth_manager(app, config.get('auth_key_manager', {}))
