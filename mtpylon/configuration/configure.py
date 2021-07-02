# -*- coding: utf-8 -*-
from typing import Optional

from aiohttp.web import Application

from mtpylon.schema import Schema
from mtpylon.sessions import SessionSubject
from mtpylon.aiohandlers import (
    create_websocket_handler,
    pub_keys_view,
    schema_view_factory,
)
from .types import (
    ConfigDict,
    RsaManagerDict,
    AuthKeyManagerDict,
    DhPrimeGeneratorDict,
    ServerSaltManagerDict,
    SessionStorageDict,
    AcknowledgmentStoreDict,
)
from .import_path import import_path
from .constants import (
    DEFAULT_RSA_MANAGER_PATH,
    DEFAULT_AUTH_KEY_MANAGER_PATH,
    DEFAULT_DH_PRIME_GENERATOR_PATH,
    DEFAULT_SERVER_SALT_MANAGER_PATH,
    DEFAULT_SESSION_STORAGE_PATH,
    DEFAULT_ACKNOWLEDGEMENT_STORAGE_PATH,
    API_VIEW,
    DEFAULT_API_PATH,
    SCHEMA_VIEW,
    PUB_KEYS_VIEW,
)
from ..constants import RSA_MANAGER_RESOURCE_NAME, \
    AUTH_KEY_MANAGER_RESOURCE_NAME, DH_PRIME_GENERATOR_RESOURCE_NAME, \
    SERVER_SALT_MANAGER_RESOURCE_NAME, SESSION_SUBJECT_RESOURCE_NAME, \
    ACKNOWLEDGEMENT_STORE_RESOURCE_NAME


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


def configure_dh_prime_generator(
    app: Application,
    config: DhPrimeGeneratorDict
):
    dh_prime_generator_path = config.get(
        'generator',
        DEFAULT_DH_PRIME_GENERATOR_PATH
    )
    dh_prime_generator = import_path(dh_prime_generator_path)

    params = config.get('params', {})

    app[DH_PRIME_GENERATOR_RESOURCE_NAME] = dh_prime_generator(**params)


def configure_serversalt_manager(
    app: Application,
    config: ServerSaltManagerDict
):
    server_salt_manager_path = config.get(
        'manager',
        DEFAULT_SERVER_SALT_MANAGER_PATH
    )
    server_salt_manager_class = import_path(server_salt_manager_path)

    params = config.get('params', {})

    app[SERVER_SALT_MANAGER_RESOURCE_NAME] = server_salt_manager_class(
        **params
    )


def configure_session_subject(
    app: Application,
    config: SessionStorageDict
):
    session_storage_path = config.get(
        'storage',
        DEFAULT_SESSION_STORAGE_PATH
    )
    session_storage_class = import_path(session_storage_path)

    params = config.get('params', {})

    app[SESSION_SUBJECT_RESOURCE_NAME] = SessionSubject(
        session_storage_factory=lambda: session_storage_class(**params)
    )


def configure_acknowledgement_store(
    app: Application,
    config: AcknowledgmentStoreDict
):
    acknowledgement_store_path = config.get(
        'storage',
        DEFAULT_ACKNOWLEDGEMENT_STORAGE_PATH
    )
    acknowledgement_store_class = import_path(acknowledgement_store_path)

    params = config.get('params', {})

    app[ACKNOWLEDGEMENT_STORE_RESOURCE_NAME] = acknowledgement_store_class(
        **params
    )


def configure_views(
    app: Application,
    schema: Schema,
    api_path: str,
    pub_keys_path: Optional[str],
    schema_path: Optional[str],
):
    app.router.add_get(
        api_path,
        create_websocket_handler(schema),
        name=API_VIEW,
    )

    if pub_keys_path is not None:
        app.router.add_get(pub_keys_path, pub_keys_view, name=PUB_KEYS_VIEW)

    if schema_path is not None:
        app.router.add_get(
            schema_path,
            schema_view_factory(schema),
            name=SCHEMA_VIEW
        )


def configure_app(
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
    configure_dh_prime_generator(app, config.get('dh_prime_generator', {}))
    configure_serversalt_manager(app, config.get('server_salt_manager', {}))
    configure_session_subject(app, config.get('session_storage', {}))
    configure_acknowledgement_store(
        app,
        config.get('acknowledgement_storage', {})
    )
    configure_views(
        app,
        schema,
        api_path=config.get('api_path', DEFAULT_API_PATH),
        pub_keys_path=config.get('pub_keys_path'),
        schema_path=config.get('schema_path')
    )
