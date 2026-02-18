#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #13: plural-as-singular unit forms not matched.

parsedatetime accepts '1 minutes ago', '1 hours ago', etc. - plural unit names
paired with cardinality 1. fast-parse-time should do the same.

Related GitHub Issue:
    #13 - Gap: plural-as-singular unit forms not matched (1 minutes ago, 1 hours ago)
    https://github.com/craigtrim/fast-parse-time/issues/13
"""

import pytest
from datetime import timedelta
from fast_parse_time import (
    parse_time_references,
    extract_relative_times,
    resolve_to_timedelta,
    extract_past_references,
    extract_future_references,
    has_temporal_info,
    parse_dates,
)


# =============================================================================
# Section 1: Past tense - bare plural-with-1 expressions (core failing cases)
# =============================================================================

def test_past_1_seconds_ago_bare():
    result = parse_time_references('1 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_past_1_minutes_ago_bare():
    result = parse_time_references('1 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_past_1_hours_ago_bare():
    result = parse_time_references('1 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_past_1_days_ago_bare():
    result = parse_time_references('1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_1_weeks_ago_bare():
    result = parse_time_references('1 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_past_1_months_ago_bare():
    result = parse_time_references('1 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_past_1_years_ago_bare():
    result = parse_time_references('1 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


# =============================================================================
# Section 2: Future tense - bare plural-with-1 expressions
# =============================================================================

def test_future_1_seconds_from_now_bare():
    result = parse_time_references('1 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_future_1_minutes_from_now_bare():
    result = parse_time_references('1 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_future_1_hours_from_now_bare():
    result = parse_time_references('1 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_future_1_days_from_now_bare():
    result = parse_time_references('1 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_future_1_weeks_from_now_bare():
    result = parse_time_references('1 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_future_1_months_from_now_bare():
    result = parse_time_references('1 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_future_1_years_from_now_bare():
    result = parse_time_references('1 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


# =============================================================================
# Section 3: Past tense - embedded in context
# =============================================================================

def test_past_1_seconds_ago_in_context():
    result = parse_time_references('alert triggered 1 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_past_1_minutes_ago_in_context():
    result = parse_time_references('show me data from 1 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_past_1_hours_ago_in_context():
    result = parse_time_references('the explosion happened 1 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_past_1_days_ago_in_context():
    result = parse_time_references('I saw it just 1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_1_weeks_ago_in_context():
    result = parse_time_references('it occurred 1 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_past_1_months_ago_in_context():
    result = parse_time_references('project started 1 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_past_1_years_ago_in_context():
    result = parse_time_references('this library was built 1 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


# =============================================================================
# Section 4: Future tense - embedded in context
# =============================================================================

def test_future_1_seconds_from_now_in_context():
    result = parse_time_references('fire in 1 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_future_1_minutes_from_now_in_context():
    result = parse_time_references('meeting starts in 1 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_future_1_hours_from_now_in_context():
    result = parse_time_references('see you in 1 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_future_1_days_from_now_in_context():
    result = parse_time_references('leave in 1 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_future_1_weeks_from_now_in_context():
    result = parse_time_references('vacation starts 1 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_future_1_months_from_now_in_context():
    result = parse_time_references('event in 1 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_future_1_years_from_now_in_context():
    result = parse_time_references('I retire in 1 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


# =============================================================================
# Section 5: Via extract_relative_times (low-level API)
# =============================================================================

def test_extract_relative_times_1_minutes_ago():
    result = extract_relative_times('1 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_hours_ago():
    result = extract_relative_times('1 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_days_ago():
    result = extract_relative_times('1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_weeks_ago():
    result = extract_relative_times('1 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_months_ago():
    result = extract_relative_times('1 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_years_ago():
    result = extract_relative_times('1 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_extract_relative_times_1_seconds_ago():
    result = extract_relative_times('1 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


# =============================================================================
# Section 6: Via resolve_to_timedelta - past gives negative delta
# =============================================================================

def test_timedelta_1_minutes_ago_is_negative():
    deltas = resolve_to_timedelta('1 minutes ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_1_hours_ago_is_negative():
    deltas = resolve_to_timedelta('1 hours ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_1_days_ago_is_negative():
    deltas = resolve_to_timedelta('1 days ago')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(days=-1)


def test_timedelta_1_weeks_ago_is_negative():
    deltas = resolve_to_timedelta('1 weeks ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_1_months_ago_is_negative():
    deltas = resolve_to_timedelta('1 months ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_1_years_ago_is_negative():
    deltas = resolve_to_timedelta('1 years ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_1_seconds_ago_is_negative():
    deltas = resolve_to_timedelta('1 seconds ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


# =============================================================================
# Section 7: Via resolve_to_timedelta - future gives positive delta
# =============================================================================

def test_timedelta_1_minutes_from_now_is_positive():
    deltas = resolve_to_timedelta('1 minutes from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_1_hours_from_now_is_positive():
    deltas = resolve_to_timedelta('1 hours from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_1_days_from_now_is_positive():
    deltas = resolve_to_timedelta('1 days from now')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(days=1)


def test_timedelta_1_weeks_from_now_is_positive():
    deltas = resolve_to_timedelta('1 weeks from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_1_months_from_now_is_positive():
    deltas = resolve_to_timedelta('1 months from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_1_years_from_now_is_positive():
    deltas = resolve_to_timedelta('1 years from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_1_seconds_from_now_is_positive():
    deltas = resolve_to_timedelta('1 seconds from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


# =============================================================================
# Section 8: Via has_temporal_info
# =============================================================================

def test_has_temporal_info_1_minutes_ago():
    assert has_temporal_info('1 minutes ago') is True


def test_has_temporal_info_1_hours_ago():
    assert has_temporal_info('1 hours ago') is True


def test_has_temporal_info_1_days_ago():
    assert has_temporal_info('1 days ago') is True


def test_has_temporal_info_1_weeks_ago():
    assert has_temporal_info('1 weeks ago') is True


def test_has_temporal_info_1_months_ago():
    assert has_temporal_info('1 months ago') is True


def test_has_temporal_info_1_years_ago():
    assert has_temporal_info('1 years ago') is True


def test_has_temporal_info_1_seconds_ago():
    assert has_temporal_info('1 seconds ago') is True


# =============================================================================
# Section 9: Via extract_past_references and extract_future_references
# =============================================================================

def test_extract_past_1_minutes_ago():
    result = extract_past_references('1 minutes ago')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_1_hours_ago():
    result = extract_past_references('1 hours ago')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_1_days_ago():
    result = extract_past_references('1 days ago')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_future_1_minutes_from_now():
    result = extract_future_references('1 minutes from now')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_1_hours_from_now():
    result = extract_future_references('1 hours from now')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_1_days_from_now():
    result = extract_future_references('1 days from now')
    assert len(result) == 1
    assert result[0].tense == 'future'


# =============================================================================
# Section 10: Via parse_dates (integrated)
# =============================================================================

def test_parse_dates_1_minutes_ago():
    result = parse_dates('report from 1 minutes ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'minute'
    assert result.relative_times[0].tense == 'past'
    assert result.has_dates is True


def test_parse_dates_1_hours_ago():
    result = parse_dates('data from 1 hours ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'hour'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_1_days_ago():
    result = parse_dates('logged 1 days ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_1_weeks_ago():
    result = parse_dates('created 1 weeks ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'week'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_1_months_ago():
    result = parse_dates('deployed 1 months ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'month'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_1_years_ago():
    result = parse_dates('founded 1 years ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'year'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_1_seconds_ago():
    result = parse_dates('fired 1 seconds ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 1
    assert result.relative_times[0].frame == 'second'
    assert result.relative_times[0].tense == 'past'


# =============================================================================
# Section 11: Regression - singular-with-1 forms still work (must not break)
# =============================================================================

def test_regression_1_second_ago_singular():
    result = parse_time_references('1 second ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_regression_1_minute_ago_singular():
    result = parse_time_references('1 minute ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_1_hour_ago_singular():
    result = parse_time_references('1 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_1_day_ago_singular():
    result = parse_time_references('1 day ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_regression_1_week_ago_singular():
    result = parse_time_references('1 week ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_regression_1_month_ago_singular():
    result = parse_time_references('1 month ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_regression_1_year_ago_singular():
    result = parse_time_references('1 year ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_regression_1_second_from_now_singular():
    result = parse_time_references('1 second from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_regression_1_minute_from_now_singular():
    result = parse_time_references('1 minute from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_regression_1_hour_from_now_singular():
    result = parse_time_references('1 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_regression_1_day_from_now_singular():
    result = parse_time_references('1 day from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_regression_1_week_from_now_singular():
    result = parse_time_references('1 week from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_regression_1_month_from_now_singular():
    result = parse_time_references('1 month from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_regression_1_year_from_now_singular():
    result = parse_time_references('1 year from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


# =============================================================================
# Section 12: Regression - plural-with-N (N>1) still works (must not break)
# =============================================================================

def test_regression_2_minutes_ago():
    result = parse_time_references('2 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_5_hours_ago():
    result = parse_time_references('5 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_10_days_ago():
    result = parse_time_references('10 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_regression_3_weeks_ago():
    result = parse_time_references('3 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_regression_6_months_ago():
    result = parse_time_references('6 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_regression_2_years_ago():
    result = parse_time_references('2 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_regression_30_seconds_ago():
    result = parse_time_references('30 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_regression_2_minutes_from_now():
    result = parse_time_references('2 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_regression_5_hours_from_now():
    result = parse_time_references('5 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_regression_10_days_from_now():
    result = parse_time_references('10 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_regression_3_weeks_from_now():
    result = parse_time_references('3 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_regression_6_months_from_now():
    result = parse_time_references('6 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_regression_2_years_from_now():
    result = parse_time_references('2 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_regression_30_seconds_from_now():
    result = parse_time_references('30 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'
