# -*- coding: utf-8 -*-
import pytest

from mtpylon.crypto import AuthKey

auth_key_tests = [
    pytest.param(
        0x4fa4120d3646e1cadc7e21fcc9c46111ff8467665908a56b18bd38bee60ee1cccc2eff69dda5e638be2b06e813e6d9832142a054d22f405d9d416f79168140d373b048f55924b836ec5be2ab92e29624edf67bd5d763f8a15c3aed587e7ac70f8fe0d78de45c4b9ea5b81a1e0a098eb064dc9609fa37ca33f703b48461aed343aabc1498dd4d1cbbf3ca4c56cc8c7dc315e251e28312ed258c74326729118251f9153f7ac9d52bd47fdf7072963f6330f06bb72e2cc744af91df3302800e80c23c25a402b97bfc5292589b1c688bd1fde0e9997d9996a32ebd39ba258137b123fa762fd07548c44fd1b9321778f6ec3464ae39402c0445bd02fa8223b30cdfc8,  # noqa
        0x189e4dd9d40b7e7b5c160c4b0313e843b05b5983,
        0x0313e843b05b5983,
        0x189e4dd9d40b7e7b,
    ),
    pytest.param(
        0x73ec5d2b95d59d33a1760dbe97870b617500cd1d05dabe2dca82306e85392e8b78f250507e1391730f6056d1bf7bcadb57bb0c34c8766a0d449e195e93e906ff8c70d77a00880939b7cea5a1bb2659d5e67d58cf8e2dd353ddac7b2b608eaeafd9fe3c44b24ba63c51bcbd50b71624bf8a25a3474fb5e848b84c143f7564cc6362ec2e83e9cd25f7b78361fe757d726ed19fbe569f91def4116ed0abafe09a6992c8d9ceb57c8527c49a1f81b0d087d96aa86dab95182d6cfd09c15f1404642b7ed61b63544918f8566044f53ce1e45fc20bad61ccf6da10b9f9d544c83f3bbaeaadbefcbee74076aeb94e3fe65b711bc727fc32dd03df5e10cbe7ceecb294ce,  # noqa
        0xce10fe6e8e29cffb284ed5662f8ba7d92e35cfa3,
        0x2f8ba7d92e35cfa3,
        0xce10fe6e8e29cffb,
    ),
    pytest.param(
        0x7190f5bcccacee71551570df063b6a4abe1bf603fd079c62351115051bfbeb00315266f9e7963970ecdb893b75f4de90ecadc2e6770cffce315d27ad58ffe9255b07373565bb3dc57f0bf398d8fd04469105faa24a8bc9498e9de4840c322a52d4a88613b2902ba031ee9b9b609912db13a459252ca9249909207193c829142bb7fdb6dd1427461d17a68541ced196763b6b3a72cf9e75b1e60405f53c1a5816adb35aa09ce334490dfb4c05a9801005b51bfdbbd52bb3a2d24d362351494d3cee71213aeda8d06c92ca2e206ed525bec6c99f53aaca6d2fff65c6a627cdb069ac4d769811f1f7d09587a718d2e472def8ce4fdcb7342531a30e894fff0f2a53,  # noqa
        0x03aa5f90a079852b27281e57fb8a0a8d4da8d551,
        0xfb8a0a8d4da8d551,
        0x03aa5f90a079852b,
    )
]


@pytest.mark.parametrize(
    'key_value,auth_key_hash,auth_key_id,auth_key_aux_hash',
    auth_key_tests
)
def test_auth_key(key_value, auth_key_hash, auth_key_id, auth_key_aux_hash):
    auth_key = AuthKey(key_value)

    assert auth_key.hash == auth_key_hash
    assert auth_key.id == auth_key_id
    assert auth_key.aux_hash == auth_key_aux_hash
