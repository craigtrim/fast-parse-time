"""Generated lookup tables, loaded only when their data is requested."""
from importlib import import_module

_TABLES = {
    'd_index_by_slot_kb': 'index_by_slot_kb',
    'd_index_by_keyterm_kb': 'index_by_keyterm_kb',
    'd_keyterm_counter_kb': 'keyterm_counter_kb',
}
__all__ = list(_TABLES)


def __getattr__(name):
    if name not in _TABLES:
        raise AttributeError(name)
    module = import_module(f'{__name__}.{_TABLES[name]}')
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
