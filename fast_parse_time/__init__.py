"""
fast-parse-time: Extract dates and times from unstructured text

This package provides a modern, comprehensive API for temporal information extraction.

Quick Start:
    >>> from fast_parse_time import parse_dates
    >>> result = parse_dates("Meeting on 04/08/2024 about issues from 5 days ago")
    >>> result.explicit_dates
    [ExplicitDate(text='04/08/2024', date_type='FULL_EXPLICIT_DATE')]
    >>> result.relative_times
    [RelativeTime(cardinality=5, frame='day', tense='past')]

For full API documentation, see the api module or README.
"""

# Import all public API functions and classes
from fast_parse_time.api import (
    # Data classes
    RelativeTime,
    ExplicitDate,
    ParseResult,
    DateType,

    # Simple high-level API (recommended for most users)
    parse_dates,
    parse_time_references,

    # Specific API functions
    extract_explicit_dates,
    extract_relative_times,
    parse_dates_with_type,
    resolve_to_datetime,
    resolve_to_timedelta,

    # Advanced functions
    extract_ambiguous_dates,
    extract_full_dates_only,
    has_temporal_info,
    extract_past_references,
    extract_future_references,

    # Recipe functions
    parse_and_resolve,
    get_date_range,
)

# Backward compatibility - keep old function name
from fast_parse_time.explicit.bp import ExplicitTimeExtractor


def extract_numeric_dates(input_text: str):
    """
    Legacy function name - use extract_explicit_dates() instead.

    This function is maintained for backward compatibility but may be
    deprecated in future versions.
    """
    return ExplicitTimeExtractor().extract_numeric_dates(input_text=input_text)


__all__ = [
    # Data classes
    'RelativeTime',
    'ExplicitDate',
    'ParseResult',
    'DateType',

    # Simple high-level API
    'parse_dates',
    'parse_time_references',

    # Specific API functions
    'extract_explicit_dates',
    'extract_relative_times',
    'parse_dates_with_type',
    'resolve_to_datetime',
    'resolve_to_timedelta',

    # Advanced functions
    'extract_ambiguous_dates',
    'extract_full_dates_only',
    'has_temporal_info',
    'extract_past_references',
    'extract_future_references',

    # Recipe functions
    'parse_and_resolve',
    'get_date_range',

    # Backward compatibility
    'extract_numeric_dates',
    'ExplicitTimeExtractor',
]
