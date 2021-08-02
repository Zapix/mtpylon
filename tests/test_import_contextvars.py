# -*- coding: utf-8 -*-
from mtpylon.contextvars import auth_key_var


def test_import_vars():
    assert auth_key_var is not None
