"""Public exports for fast-parse-time, loaded on demand."""
from importlib import import_module

__all__ = [
    'RelativeTime', 'ExplicitDate', 'ParseResult', 'ParsedDate', 'DateType',
    'parse_dates', 'parse_time_references', 'extract_explicit_dates',
    'extract_date_strings', 'parse_date_strings', 'extract_relative_times',
    'parse_dates_with_type', 'resolve_to_datetime', 'resolve_to_timedelta',
    'extract_ambiguous_dates', 'extract_full_dates_only', 'has_temporal_info',
    'extract_past_references', 'extract_future_references', 'parse_and_resolve',
    'get_date_range', 'extract_numeric_dates', 'ExplicitTimeExtractor',
]
_MODELS = {'RelativeTime', 'ExplicitDate', 'ParseResult', 'ParsedDate', 'DateType'}


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
    module = import_module('.models' if name in _MODELS else '.api', __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
