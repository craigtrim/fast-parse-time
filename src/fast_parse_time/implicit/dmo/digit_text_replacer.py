"""Compatibility imports; implementation lives in fast_parse_time.implicit.normalization."""
from importlib import import_module


def __getattr__(name):
    if name.startswith('__'):
        raise AttributeError(name)
    value = getattr(import_module('fast_parse_time.implicit.normalization'), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(dir(import_module('fast_parse_time.implicit.normalization'))))
