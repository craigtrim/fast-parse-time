#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Public API for fast-parse-time

This module provides a clean, comprehensive API for extracting temporal information
from text. It exposes all useful permutations while maintaining clarity.

Design principles:
- Simple functions for common use cases
- Consistent return types (never None, always structured)
- Clear naming that indicates functionality
- Type hints for IDE support
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from fast_parse_time.explicit.dto import DateType
from fast_parse_time.explicit.bp import ExplicitTimeExtractor
from fast_parse_time.implicit.svc import AnalyzeTimeReferences, ResolveTimeReferences


# ============================================================================
# Data Classes for Return Types
# ============================================================================

@dataclass
class RelativeTime:
    """Represents a relative time reference like '5 days ago'"""
    cardinality: int
    frame: str  # 'day', 'week', 'month', 'year', 'hour', 'minute', 'second'
    tense: str  # 'past' or 'future'

    def to_timedelta(self) -> timedelta:
        """Convert to Python timedelta object"""
        # Use the internal _get_timedelta method directly for cleaner conversion
        solution = {
            'Cardinality': self.cardinality,
            'Frame': self.frame,
            'Tense': self.tense
        }
        return ResolveTimeReferences._get_timedelta(solution)

    def to_datetime(self, reference: Optional[datetime] = None) -> datetime:
        """
        Convert to absolute datetime

        Args:
            reference: Reference point for calculation (defaults to now)
        """
        if reference is None:
            reference = datetime.now()
        delta = self.to_timedelta()
        # Note: to_timedelta() already handles the sign based on tense
        # (past = negative, future = positive)
        return reference + delta


@dataclass
class ExplicitDate:
    """Represents an explicit date found in text"""
    text: str  # Original text (e.g., '04/08/2024')
    date_type: str  # DateType name (e.g., 'FULL_EXPLICIT_DATE')


@dataclass
class ParseResult:
    """Combined result containing all temporal information found"""
    explicit_dates: List[ExplicitDate]
    relative_times: List[RelativeTime]

    @property
    def has_dates(self) -> bool:
        """Returns True if any temporal information was found"""
        return len(self.explicit_dates) > 0 or len(self.relative_times) > 0


# ============================================================================
# Simple High-Level API (Most Common Use Cases)
# ============================================================================

def parse_dates(text: str) -> ParseResult:
    """
    Extract all temporal information from text (both explicit and relative).

    This is the simplest, most comprehensive function - use this if you want
    to find all date/time references in text.

    Args:
        text: Input text to parse

    Returns:
        ParseResult containing both explicit dates and relative time references

    Example:
        >>> result = parse_dates("Meeting on 04/08/2024 about issues from 5 days ago")
        >>> result.explicit_dates
        [ExplicitDate(text='04/08/2024', date_type='FULL_EXPLICIT_DATE')]
        >>> result.relative_times
        [RelativeTime(cardinality=5, frame='day', tense='past')]
    """
    explicit = extract_explicit_dates(text)
    relative = extract_relative_times(text)

    explicit_list = [
        ExplicitDate(text=date_str, date_type=date_type)
        for date_str, date_type in explicit.items()
    ]

    return ParseResult(
        explicit_dates=explicit_list,
        relative_times=relative
    )


def parse_time_references(text: str) -> List[RelativeTime]:
    """
    Extract only relative time references (like '5 days ago', 'next week').

    Use this when you only care about relative time expressions, not explicit dates.

    Args:
        text: Input text to parse

    Returns:
        List of RelativeTime objects

    Example:
        >>> parse_time_references("Show me data from 5 days ago and last week")
        [RelativeTime(cardinality=5, frame='day', tense='past'),
         RelativeTime(cardinality=1, frame='week', tense='past')]
    """
    return extract_relative_times(text)


# ============================================================================
# Specific API Functions (For Precise Control)
# ============================================================================

def extract_explicit_dates(text: str) -> Dict[str, str]:
    """
    Extract explicit/numeric dates from text.

    Finds dates in formats like:
    - Full dates: 04/08/2024, 06-05-2016, March 15, 2024
    - Partial dates: 3/24, 12/2023
    - Ambiguous dates: 4/8 (could be April 8 or August 4)
    - Written month formats: March 15, 2024, 15 March 2024, Mar 15, 2024

    Args:
        text: Input text to parse

    Returns:
        Dictionary mapping date strings to their DateType classification
        Empty dict if no dates found

    Example:
        >>> extract_explicit_dates("Event on 04/08/2024")
        {'04/08/2024': 'FULL_EXPLICIT_DATE'}
        >>> extract_explicit_dates("Event on March 15, 2024")
        {'March 15, 2024': 'FULL_EXPLICIT_DATE'}
    """
    extractor = ExplicitTimeExtractor()

    # Try numeric dates first
    result = extractor.extract_numeric_dates(input_text=text)
    if result is None:
        result = {}

    # Also try written month formats
    written_result = extractor.extract_written_dates(input_text=text)
    if written_result:
        result.update(written_result)

    return result


def extract_relative_times(text: str) -> List[RelativeTime]:
    """
    Extract relative time references from text.

    Finds expressions like:
    - '5 days ago'
    - 'last week'
    - 'next 3 months'
    - 'couple of hours ago'

    Args:
        text: Input text to parse

    Returns:
        List of RelativeTime objects (empty list if none found)

    Example:
        >>> extract_relative_times("Show records from 5 days ago")
        [RelativeTime(cardinality=5, frame='day', tense='past')]
    """
    analyzer = AnalyzeTimeReferences()
    result = analyzer.process(text)

    relative_times = []
    for item in result.get('result', []):
        relative_times.append(RelativeTime(
            cardinality=item['Cardinality'],
            frame=item['Frame'],
            tense=item['Tense']
        ))

    return relative_times


def parse_dates_with_type(text: str, date_type: Optional[str] = None) -> Dict[str, str]:
    """
    Extract explicit dates, optionally filtering by type.

    Args:
        text: Input text to parse
        date_type: Optional DateType to filter by (e.g., 'FULL_EXPLICIT_DATE')

    Returns:
        Dictionary of matching dates

    Example:
        >>> parse_dates_with_type("Event 04/08/2024 or maybe 3/24", 'FULL_EXPLICIT_DATE')
        {'04/08/2024': 'FULL_EXPLICIT_DATE'}
    """
    all_dates = extract_explicit_dates(text)

    if date_type is None:
        return all_dates

    return {
        date_str: dtype
        for date_str, dtype in all_dates.items()
        if dtype == date_type
    }


def resolve_to_datetime(
    text: str,
    reference: Optional[datetime] = None
) -> List[datetime]:
    """
    Extract relative time references and convert to absolute datetimes.

    This is a convenience function that combines extraction and resolution
    into a single step.

    Args:
        text: Input text to parse
        reference: Reference point for calculation (defaults to now)

    Returns:
        List of datetime objects

    Example:
        >>> resolve_to_datetime("Show me data from 5 days ago")
        [datetime.datetime(2025, 11, 14, ...)]  # 5 days before now
    """
    relative_times = extract_relative_times(text)
    return [rt.to_datetime(reference) for rt in relative_times]


def resolve_to_timedelta(text: str) -> List[timedelta]:
    """
    Extract relative time references and convert to timedelta objects.

    Use this when you need the duration/offset rather than absolute datetimes.

    Args:
        text: Input text to parse

    Returns:
        List of timedelta objects

    Example:
        >>> resolve_to_timedelta("5 days ago")
        [timedelta(days=5)]
    """
    relative_times = extract_relative_times(text)
    return [rt.to_timedelta() for rt in relative_times]


# ============================================================================
# Advanced API Functions (Power User Recipes)
# ============================================================================

def extract_ambiguous_dates(text: str) -> Dict[str, str]:
    """
    Extract only ambiguous dates that need clarification.

    Useful when you want to prompt users for clarification on dates
    like '4/8' which could be April 8 or August 4.

    Args:
        text: Input text to parse

    Returns:
        Dictionary of ambiguous dates only

    Example:
        >>> extract_ambiguous_dates("Meeting 4/8 or 04/08/2024")
        {'4/8': 'DAY_MONTH_AMBIGUOUS'}
    """
    return parse_dates_with_type(text, 'DAY_MONTH_AMBIGUOUS')


def extract_full_dates_only(text: str) -> Dict[str, str]:
    """
    Extract only complete dates (with year, month, and day).

    Args:
        text: Input text to parse

    Returns:
        Dictionary of full dates only

    Example:
        >>> extract_full_dates_only("Event 04/08/2024 or maybe 3/24")
        {'04/08/2024': 'FULL_EXPLICIT_DATE'}
    """
    return parse_dates_with_type(text, 'FULL_EXPLICIT_DATE')


def has_temporal_info(text: str) -> bool:
    """
    Quick check if text contains any temporal information.

    More efficient than full parsing if you only need a yes/no answer.

    Args:
        text: Input text to check

    Returns:
        True if any dates or time references found

    Example:
        >>> has_temporal_info("Meeting tomorrow")
        False  # 'tomorrow' not currently supported
        >>> has_temporal_info("Meeting on 04/08/2024")
        True
    """
    result = parse_dates(text)
    return result.has_dates


def extract_past_references(text: str) -> List[RelativeTime]:
    """
    Extract only past time references ('5 days ago', 'last week').

    Args:
        text: Input text to parse

    Returns:
        List of RelativeTime objects with tense='past'

    Example:
        >>> extract_past_references("Show data from 5 days ago and next week")
        [RelativeTime(cardinality=5, frame='day', tense='past')]
    """
    all_times = extract_relative_times(text)
    return [rt for rt in all_times if rt.tense == 'past']


def extract_future_references(text: str) -> List[RelativeTime]:
    """
    Extract only future time references ('next week', 'in 3 days').

    Args:
        text: Input text to parse

    Returns:
        List of RelativeTime objects with tense='future'

    Example:
        >>> extract_future_references("Reminder in 5 days and last week")
        [RelativeTime(cardinality=5, frame='day', tense='future')]
    """
    all_times = extract_relative_times(text)
    return [rt for rt in all_times if rt.tense == 'future']


# ============================================================================
# Recipe Functions (Common Patterns)
# ============================================================================

def parse_and_resolve(text: str, reference: Optional[datetime] = None) -> Dict[str, List[datetime]]:
    """
    Parse all temporal info and resolve relative times to absolute datetimes.

    This is a common recipe that combines explicit date extraction with
    relative time resolution.

    Args:
        text: Input text to parse
        reference: Reference point for relative time calculation

    Returns:
        Dictionary with 'explicit' (date strings) and 'resolved' (datetimes) keys

    Example:
        >>> parse_and_resolve("Meeting 04/08/2024 about issues from 5 days ago")
        {
            'explicit': ['04/08/2024'],
            'resolved': [datetime.datetime(2025, 11, 14, ...)]
        }
    """
    result = parse_dates(text)
    resolved = [rt.to_datetime(reference) for rt in result.relative_times]

    return {
        'explicit': [ed.text for ed in result.explicit_dates],
        'resolved': resolved
    }


def get_date_range(text: str) -> Optional[tuple[datetime, datetime]]:
    """
    Extract a date range from text containing two relative time references.

    Useful for queries like "show me data from 7 days ago to 3 days ago".

    Args:
        text: Input text to parse

    Returns:
        Tuple of (start_date, end_date) if two references found, None otherwise

    Example:
        >>> get_date_range("data from 7 days ago to 3 days ago")
        (datetime(...), datetime(...))  # 7 days ago to 3 days ago
    """
    times = extract_relative_times(text)

    if len(times) != 2:
        return None

    datetimes = [t.to_datetime() for t in times]
    return (min(datetimes), max(datetimes))


# ============================================================================
# Exports
# ============================================================================

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
]
