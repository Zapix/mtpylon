# -*- coding: utf-8 -*-
import rsa  # type: ignore
from mtpylon.crypto.rsa import encrypt, decrypt


private_key_str = """
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAOUO55aK9gVcATy6lngUfo4HahczT5Q/uNRgPSENHB2VnRV4JDVh
B083bhWACJGQQMupGg+KrRKptaq14NJdqCkCAwEAAQJANk9xY8VxDdZByNdo4/Hg
C+cAJZ4Z6UmullR3SgXku7KR42b2mVuyKSeBCrOWGfUSun1h4iU/JGZu30Q6qlhZ
AQIhAPV0QgVXU1EXfE/fixx7G9Y7mScGWmyKrByWdY5YAEnJAiEA7uZPA4fWMzaq
ZJqKbuM/ovZ3kaU3zyiG4IB0jEttm2ECIQDt1R57qmfStV0Az+wtRqRsawc1JxTL
A3tNoAR8TozI8QIhAIm7jmJitkPgiGxoDNfRfKbfoh/+OSbeHqTgalFYS2EBAiAX
5ZV28dPweHv1syNn588tMIzcES2BjE6KU7Q8qM8Saw==
-----END RSA PRIVATE KEY-----
"""
private_key = rsa.PrivateKey.load_pkcs1(private_key_str)


public_key_str = """
-----BEGIN RSA PUBLIC KEY-----
MEgCQQDlDueWivYFXAE8upZ4FH6OB2oXM0+UP7jUYD0hDRwdlZ0VeCQ1YQdPN24V
gAiRkEDLqRoPiq0SqbWqteDSXagpAgMBAAE=
-----END RSA PUBLIC KEY-----
"""
public_key = rsa.PublicKey.load_pkcs1(public_key_str)


original_data = b'hello world'

encrypted_data = (
    b'h\xb7\xd2V\xee.\xbdPi%(\x05\xfd\xd4\x13'
    b'\xae%~V\x99\xf7wW\x0c\xd2\xac|\x11' +
    b'\x0e8\xb29\xbe\xce\xc2\xcaI\xe5\x1c' +
    b'$6\x7f[\xc3e\xf0\x85\x1b2\xe2O\xfa' +
    b"H\x98\xa1\x99'\xf05y\x94\x8d\xba\xf4"
)


def test_encrypt_rsa():
    assert encrypt(original_data, public_key) == encrypted_data


def test_decrypt_rsa():
    assert decrypt(encrypted_data, private_key) == original_data
