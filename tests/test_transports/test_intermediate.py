# -*- coding: utf-8 -*-
from mtpylon.transports.intermediate import wrap, unwrap


original_message = b'\x47\xac\x9f\xf1\xf1\x7d\xd4\xc0\xcd\xde\xdf\x86\xad\x73'
wrapped_message = b'\x0e\x00\x00\x00' + original_message


def test_wrap():
    returned_message = wrap(original_message)

    assert returned_message == wrapped_message


def test_unwrap():
    returned_message = unwrap(wrapped_message)

    assert returned_message == original_message
