# -*- coding: utf-8 -*-
import pytest
from inspect import isfunction

from mtpylon.configuration.import_path import import_path


def test_import_path_empty():
    with pytest.raises(ValueError):
        import_path('')


def test_import_path_only_item_passed():
    with pytest.raises(ValueError):
        import_path('item')


def test_only_absolute_path_allowed():
    with pytest.raises(ValueError):
        import_path('.relative.module.import.path')


def test_wrong_module_path():
    with pytest.raises(ModuleNotFoundError):
        import_path('wrong.module.Item')


def test_wrong_module_attribute():
    with pytest.raises(ValueError):
        import_path('xml.dom.minidom.wrong_attr')


def test_correct_import():
    parse = import_path('xml.dom.minidom.parse')
    assert isfunction(parse)
