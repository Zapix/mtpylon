# -*- coding: utf-8 -*-
from typing import Any
from importlib import import_module

from .types import ImportPath


def import_path(path: ImportPath) -> Any:
    """
    Imports item from absolute path.
    """
    if path == '':
        raise ValueError('Path shouldn`t been empty string')

    if path[0] == '.':
        raise ValueError('Only absolute import are allowed')

    *module_path_list, item = path.split('.')

    if len(module_path_list) == 0:
        raise ValueError('Module path hasn`t been passed')

    module_path = '.'.join(module_path_list)

    current_module = import_module(module_path)

    value = getattr(current_module, item, None)

    if value is None:
        raise ValueError(f'{item} not found in {module_path}')

    return value
