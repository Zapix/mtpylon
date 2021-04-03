# -*- coding: utf-8 -*-
import pytest

from mtpylon.transports import get_wrapper
from mtpylon.transports.intermediate import PROTOCOL_TAG, wrapper


def test_wrong_wrapper():
    with pytest.raises(ValueError):
        get_wrapper(123123)


def test_ok():
    assert get_wrapper(PROTOCOL_TAG) == wrapper
