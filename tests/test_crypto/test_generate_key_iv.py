# -*- coding: utf-8 -*-
from mtpylon import int128
from mtpylon.crypto import AuthKey
from mtpylon.crypto.generate_key_iv import generate_key_iv


auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key = AuthKey(auth_key_data)

msg_key = int128(274926916796624172065190426750279701994)


expected_servers_key = (
    b'\xa9,0\x8a\x034\x01$\x16"\xc8\xf5}\x03\x14>\xe6\xef%\xbfvj\xd5\x81' +
    b'\x8b\xb0#\xf9\xb5^\x027'
)

expected_servers_iv = (
    b'd\xf9\xcc\x03T\x84\x86\xc2\x84\xbc\xb7\xdb\x07\x05u\xc1\x90Y\x9a)\xf6' +
    b'Xv\xf6\x12d\t\xe4i\x85\xff\xea'
)

expected_clients_key = (
    b"'\xf9\xaf\xfc\x05\x9e\xc4NgIx\x1d\xb0W\xd3\x84.\xf8\xcd3\xb2\xa4}\x8c" +
    b'\x00\x93\xe7\x10\xc2\x98\xefx'
)

expected_clients_iv = (
    b'\x93\xfa\xf0\xf1\x81\xae\xa1\xa6\xac\xdc\xce\xed\x89\x8d\x12\x17' +
    b'\xf4\x0e\x92|\xa2\x8b\x04\x83\x9e\x16\xb76pS\x9bz'
)


def test_generate_servers_key_iv():
    key_pair = generate_key_iv(auth_key, msg_key)

    assert key_pair.key == expected_servers_key
    assert key_pair.iv == expected_servers_iv


def test_generate_clients_key_iv():
    key_pair = generate_key_iv(auth_key, msg_key, key_type='client')

    assert key_pair.key == expected_clients_key
    assert key_pair.iv == expected_clients_iv
