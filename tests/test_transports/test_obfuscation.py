# -*- coding: utf-8 -*-
from mtpylon.transports.obfuscation import parse_header

from ..helpers import hexstr_to_bytes


init_buffer = hexstr_to_bytes(
    'ac12ac1df7f68e2eacd4085138d294d7f9d71000469b9fbdc6cf0cbb50382a5d34a38c29ae4e14945dded705a65625e02e206e7a12f9e13aeeeeeeeece9fb887'  # noqa
)

reversed_init_buffer = hexstr_to_bytes(
    '87b89fceeeeeeeee3ae1f9127a6e202ee02556a605d7de5d94144eae298ca3345d2a3850bb0ccfc6bd9f9b460010d7f9d794d2385108d4ac2e8ef6f71dac12ac'  # noqa
)

encrypted_init_buffer = hexstr_to_bytes(
    '40a75bc91ea1eb6f367241fbfe013c2e56acc740dde85e8d7796af83763b552e567443c3780a6e96a5bd457b711c9a52963c217d99f8b8dc6bdb572fe929ec85'  # noqa
)

client_key = hexstr_to_bytes(
    'acd4085138d294d7f9d71000469b9fbdc6cf0cbb50382a5d34a38c29ae4e1494'
)

client_iv = hexstr_to_bytes(
    '5dded705a65625e02e206e7a12f9e13a'
)

server_key = hexstr_to_bytes(
    '3ae1f9127a6e202ee02556a605d7de5d94144eae298ca3345d2a3850bb0ccfc6'

)

server_iv = hexstr_to_bytes(
    'bd9f9b460010d7f9d794d2385108d4ac'
)

header = hexstr_to_bytes(
    'ac12ac1df7f68e2eacd4085138d294d7f9d71000469b9fbdc6cf0cbb50382a5d34a38c29ae4e14945dded705a65625e02e206e7a12f9e13a6bdb572fe929ec85'  # noqa
)

client_original_msg = hexstr_to_bytes(
    '280000000000000000000000040000005e595260140000007897466054b3ae2f3172ad489eef5aa8271f730e'  # noqa
)

client_encrypted_msg = hexstr_to_bytes(
    'e7dbc655fbf3234c5f265c50c06482bd55ac73a906fdfee24b946ea3d268e42e11a1fccac23884200ffb7e67'  # noqa
)

server_original_message = hexstr_to_bytes(
    '54000000000000000000000001f442f55e595260400000006324160554b3ae2f3172ad489eef5aa8271f730e857a0d1dc11006c19103166c8b21d22b082690282a15c9613d00000015c4b51c01000000216be86c022bb4c3'  # noqa
)

server_encrypted_msg = hexstr_to_bytes(
    'fb4209d8ae8eb555348b62e53c0df46e0bb3fc0dd8b8c676c8abd9200e5546d61997e1e8473bb39304afa06ab84a4cee580541bd99bdb602737e4d358ac5c609451b2234720d93120a37b9c0b460e626d27d9da196c4690c'  # noqa
)


def test_parsed_header():
    transport_tag, obfuscator = parse_header(header)

    assert transport_tag == 0xeeeeeeee
    assert obfuscator.client_key == client_key
    assert obfuscator.client_iv == client_iv
    assert obfuscator.server_key == server_key
    assert obfuscator.server_iv == server_iv


def test_decrypt_client_message():
    transport_tag, obfuscator = parse_header(header)

    assert obfuscator.decrypt(client_encrypted_msg) == client_original_msg


def test_encrypt_server_message():
    transport_tag, obfuscator = parse_header(header)

    assert obfuscator.encrypt(server_original_message) == server_encrypted_msg
