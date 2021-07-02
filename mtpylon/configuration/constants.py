# -*- coding: utf-8 -*-
DEFAULT_RSA_MANAGER_PATH = 'mtpylon.crypto.rsa_manager.RsaManager'

DEFAULT_AUTH_KEY_MANAGER_PATH = \
    'mtpylon.crypto.auth_key_manager.AuthKeyManager'

DEFAULT_DH_PRIME_GENERATOR_PATH = \
    'mtpylon.dh_prime_generators.two_ton.generate'

DEFAULT_SERVER_SALT_MANAGER_PATH = 'mtpylon.salts.ServerSaltManager'

DEFAULT_SESSION_STORAGE_PATH = 'mtpylon.sessions.InMemorySessionStorage'

DEFAULT_ACKNOWLEDGEMENT_STORAGE_PATH = \
    'mtpylon.acknowledgement_store.InmemoryAcknowledgementStore'


API_VIEW = 'mtpylon_api_view'  # name of mtpylon api view in aiohttp
DEFAULT_API_PATH = '/ws'
PUB_KEYS_VIEW = 'mtpylon_pub_keys_view'  # name of pub keys view in aiohttp
SCHEMA_VIEW = 'mtpylon_schema_view'  # name of schema view in aiohttp
