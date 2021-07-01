# -*- coding: utf-8 -*-
RSA_MANAGER_RESOURCE_NAME = 'rsa_manager'  # name of rsa manager in asyncio app
DEFAULT_RSA_MANAGER_PATH = 'mtpylon.crypto.rsa_manager.RsaManager'

AUTH_KEY_MANAGER_RESOURCE_NAME = 'auth_key_manager'
DEFAULT_AUTH_KEY_MANAGER_PATH = \
    'mtpylon.crypto.auth_key_manager.AuthKeyManager'


DH_PRIME_GENERATOR_RESOURCE_NAME = 'dh_prime_generator'
DEFAULT_DH_PRIME_GENERATOR_PATH = \
    'mtpylon.dh_prime_generators.two_ton.generate'


SERVER_SALT_MANAGER_RESOURCE_NAME = 'server_salt_manager'
DEFAULT_SERVER_SALT_MANAGER_PATH = 'mtpylon.salts.ServerSaltManager'

SESSION_SUBJECT_RESOURCE_NAME = 'session_subject'
DEFAULT_SESSION_STORAGE_PATH = 'mtpylon.sessions.InMemorySessionStorage'

ACKNOWLEDGEMENT_STORE_RESOURCE_NAME = 'acknowledgement_store'
DEFAULT_ACKNOWLEDGEMENT_STORAGE_PATH = \
    'mtpylon.acknowledgement_store.InmemoryAcknowledgementStore'
