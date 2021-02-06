# -*- coding: utf-8 -*-

class InvalidCombinator(Exception):
    """
    Raised when wrong combinator has been passed
    """
    pass


class InvalidConstructor(Exception):
    """
    Raised when wrong constructor has been passed
    """
    pass


class InvalidFunction(Exception):
    """
    Raises when wrong mtpytlon function has been passed
    """
    pass


class SchemaChangeError(Exception):
    """
    Raises when user tries add or delete combinator, function after schema
    initialization
    """


class DumpError(Exception):
    """
    Raises error when can't dump object or function call  by schema
    """
    pass
