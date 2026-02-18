#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Test the new unified API"""

from datetime import datetime, timedelta
from fast_parse_time import (
    parse_dates,
    parse_time_references,
    extract_explicit_dates,
    extract_relative_times,
    resolve_to_datetime,
    resolve_to_timedelta,
    extract_past_references,
    extract_future_references,
    extract_full_dates_only,
    extract_ambiguous_dates,
    has_temporal_info,
    parse_and_resolve,
    RelativeTime,
    ExplicitDate,
)


def test_parse_dates():
    """Test the high-level parse_dates function"""
    result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')

    assert len(result.explicit_dates) == 1
    assert result.explicit_dates[0].text == '04/08/2024'
    assert result.explicit_dates[0].date_type == 'FULL_EXPLICIT_DATE'

    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 5
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'past'

    assert result.has_dates is True


def test_parse_time_references():
    """Test parsing only time references"""
    times = parse_time_references('show me data from 5 days ago')

    assert len(times) == 1
    assert times[0].cardinality == 5
    assert times[0].frame == 'day'
    assert times[0].tense == 'past'


def test_extract_explicit_dates():
    """Test extracting only explicit dates"""
    dates = extract_explicit_dates('Event on 04/08/2024 or maybe 3/24')

    assert len(dates) == 2
    assert dates['04/08/2024'] == 'FULL_EXPLICIT_DATE'
    assert dates['3/24'] == 'MONTH_DAY'


def test_extract_relative_times():
    """Test extracting relative times"""
    times = extract_relative_times('show records from 5 days ago')

    assert len(times) == 1
    assert isinstance(times[0], RelativeTime)
    assert times[0].cardinality == 5


def test_resolve_to_datetime():
    """Test resolving to datetime objects"""
    datetimes = resolve_to_datetime('5 days ago')

    assert len(datetimes) == 1
    assert isinstance(datetimes[0], datetime)


def test_resolve_to_timedelta():
    """Test resolving to timedelta objects"""
    deltas = resolve_to_timedelta('5 days ago')

    assert len(deltas) == 1
    assert isinstance(deltas[0], timedelta)


def test_extract_past_references():
    """Test filtering only past references"""
    # Note: 'next week' is future, not currently supported by the library
    past = extract_past_references('from 5 days ago')

    assert len(past) == 1
    assert past[0].tense == 'past'


def test_extract_full_dates_only():
    """Test extracting only full dates"""
    full_dates = extract_full_dates_only('Event 04/08/2024 or maybe 3/24')

    assert len(full_dates) == 1
    assert '04/08/2024' in full_dates
    assert '3/24' not in full_dates


def test_extract_ambiguous_dates():
    """Test extracting ambiguous dates"""
    ambiguous = extract_ambiguous_dates('Meeting 4/8 or 04/08/2024')

    assert '4/8' in ambiguous
    assert '04/08/2024' not in ambiguous


def test_has_temporal_info():
    """Test quick check for temporal info"""
    assert has_temporal_info('Meeting on 04/08/2024') is True
    assert has_temporal_info('Just a regular sentence') is False


def test_parse_and_resolve():
    """Test the recipe function"""
    result = parse_and_resolve('Meeting 04/08/2024 about issues from 5 days ago')

    assert len(result['explicit']) == 1
    assert '04/08/2024' in result['explicit']

    assert len(result['resolved']) == 1
    assert isinstance(result['resolved'][0], datetime)


def test_relative_time_to_datetime():
    """Test RelativeTime dataclass methods"""
    rt = RelativeTime(cardinality=5, frame='day', tense='past')

    # Test to_timedelta
    delta = rt.to_timedelta()
    assert isinstance(delta, timedelta)

    # Test to_datetime
    ref = datetime(2025, 11, 19, 12, 0, 0)
    dt = rt.to_datetime(reference=ref)
    assert isinstance(dt, datetime)
    assert dt < ref  # Past tense should be before reference


def test_backward_compatibility():
    """Test that old API still works"""
    from fast_parse_time import extract_numeric_dates

    result = extract_numeric_dates('Meeting on 3/24')
    assert result == {'3/24': 'MONTH_DAY'}


if __name__ == '__main__':
    test_parse_dates()
    test_parse_time_references()
    test_extract_explicit_dates()
    test_extract_relative_times()
    test_resolve_to_datetime()
    test_resolve_to_timedelta()
    test_extract_past_references()
    test_extract_full_dates_only()
    test_extract_ambiguous_dates()
    test_has_temporal_info()
    test_parse_and_resolve()
    test_relative_time_to_datetime()
    test_backward_compatibility()
    print('All new API tests passed!')
