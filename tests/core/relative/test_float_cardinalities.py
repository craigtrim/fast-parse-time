#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #15: Float/decimal cardinalities not supported.

parsedatetime accepts floating-point values as cardinalities. fast-parse-time
must accept inputs like '7.2 days ago', '22.355 hours ago', '4.8 months ago'
and return a rounded integer cardinality.

Rounding rule: Python built-in round() (banker's rounding).
    - 7.2  → 7,  7.8  → 8
    - 2.5  → 2,  3.5  → 4  (round half to even)
    - 4.8  → 5,  22.355 → 22

Covered forms:
    - X.X [unit] ago            (explicit past)
    - X.X [unit] from now       (explicit future)
    - [unit] abbreviations with floats (hrs, mins, secs, wks, yrs, mos)

Covered units: seconds, minutes, hours, days, weeks, months, years

Out of scope:
    - Compound multi-unit ('1.5 years 2 months') → issue #20
    - ISO 8601 fractional seconds → issue #23
    - Decade → issue #19

Related GitHub Issues:
    #15 - Gap: float/decimal cardinalities not supported
    https://github.com/craigtrim/fast-parse-time/issues/15
"""

import pytest
from datetime import timedelta
from fast_parse_time import (
    parse_time_references,
    extract_relative_times,
    extract_past_references,
    extract_future_references,
    has_temporal_info,
    resolve_to_timedelta,
    parse_dates,
)


# =============================================================================
# Section 1: Past tense (ago) — days
# =============================================================================

def test_float_days_past_7_2():
    result = parse_time_references('7.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_7_8():
    result = parse_time_references('7.8 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_1_4():
    result = parse_time_references('1.4 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_2_1():
    result = parse_time_references('2.1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_3_3():
    result = parse_time_references('3.3 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_5_7():
    result = parse_time_references('5.7 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_14_2():
    result = parse_time_references('14.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 14
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_30_6():
    result = parse_time_references('30.6 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_0_9():
    result = parse_time_references('0.9 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_100_4():
    result = parse_time_references('100.4 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 100
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_10_6():
    result = parse_time_references('10.6 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 11
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_21_3():
    result = parse_time_references('21.3 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 21
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_90_8():
    result = parse_time_references('90.8 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 91
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_365_2():
    result = parse_time_references('365.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 365
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_days_past_6_6():
    result = parse_time_references('6.6 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 2: Past tense (ago) — minutes
# =============================================================================

def test_float_minutes_past_58_4():
    result = parse_time_references('58.4 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 58
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_30_7():
    result = parse_time_references('30.7 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_15_2():
    result = parse_time_references('15.2 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_45_8():
    result = parse_time_references('45.8 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 46
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_10_1():
    result = parse_time_references('10.1 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_2_7():
    result = parse_time_references('2.7 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_90_3():
    result = parse_time_references('90.3 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 90
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_5_9():
    result = parse_time_references('5.9 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_1_4():
    result = parse_time_references('1.4 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_120_6():
    result = parse_time_references('120.6 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 121
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_0_9():
    result = parse_time_references('0.9 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_minutes_past_59_9():
    result = parse_time_references('59.9 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 60
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


# =============================================================================
# Section 3: Past tense (ago) — hours
# =============================================================================

def test_float_hours_past_8_3():
    result = parse_time_references('8.3 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_22_355():
    result = parse_time_references('22.355 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 22
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_3_7():
    result = parse_time_references('3.7 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_12_2():
    result = parse_time_references('12.2 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_6_8():
    result = parse_time_references('6.8 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_0_9():
    result = parse_time_references('0.9 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_2_4():
    result = parse_time_references('2.4 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_4_6():
    result = parse_time_references('4.6 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_18_1():
    result = parse_time_references('18.1 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 18
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_23_9():
    result = parse_time_references('23.9 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 24
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_1_3():
    result = parse_time_references('1.3 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_hours_past_10_7():
    result = parse_time_references('10.7 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 11
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


# =============================================================================
# Section 4: Past tense (ago) — weeks
# =============================================================================

def test_float_weeks_past_1_4():
    result = parse_time_references('1.4 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_2_3():
    result = parse_time_references('2.3 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_3_7():
    result = parse_time_references('3.7 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_0_8():
    result = parse_time_references('0.8 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_4_2():
    result = parse_time_references('4.2 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_1_1():
    result = parse_time_references('1.1 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_2_9():
    result = parse_time_references('2.9 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_weeks_past_8_2():
    result = parse_time_references('8.2 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


# =============================================================================
# Section 5: Past tense (ago) — months
# =============================================================================

def test_float_months_past_1_4():
    result = parse_time_references('1.4 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_4_8():
    result = parse_time_references('4.8 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_2_6():
    result = parse_time_references('2.6 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_3_3():
    result = parse_time_references('3.3 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_0_7():
    result = parse_time_references('0.7 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_8_2():
    result = parse_time_references('8.2 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_11_1():
    result = parse_time_references('11.1 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 11
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_6_4():
    result = parse_time_references('6.4 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_months_past_9_8():
    result = parse_time_references('9.8 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


# =============================================================================
# Section 6: Past tense (ago) — years
# =============================================================================

def test_float_years_past_5_11553():
    result = parse_time_references('5.11553 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_1_4():
    result = parse_time_references('1.4 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_2_7():
    result = parse_time_references('2.7 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_3_8():
    result = parse_time_references('3.8 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_0_6():
    result = parse_time_references('0.6 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_4_2():
    result = parse_time_references('4.2 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_7_3():
    result = parse_time_references('7.3 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_0_9():
    result = parse_time_references('0.9 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_years_past_1_1():
    result = parse_time_references('1.1 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


# =============================================================================
# Section 7: Past tense (ago) — seconds
# =============================================================================

def test_float_seconds_past_10_3():
    result = parse_time_references('10.3 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_30_7():
    result = parse_time_references('30.7 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_45_2():
    result = parse_time_references('45.2 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_2_4():
    result = parse_time_references('2.4 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_5_6():
    result = parse_time_references('5.6 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_15_1():
    result = parse_time_references('15.1 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_0_9():
    result = parse_time_references('0.9 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_seconds_past_59_8():
    result = parse_time_references('59.8 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 60
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


# =============================================================================
# Section 8: Future tense (from now) — days
# =============================================================================

def test_float_days_future_7_2():
    result = parse_time_references('7.2 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_3_8():
    result = parse_time_references('3.8 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_14_2():
    result = parse_time_references('14.2 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 14
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_1_3():
    result = parse_time_references('1.3 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_21_6():
    result = parse_time_references('21.6 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 22
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_0_9():
    result = parse_time_references('0.9 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_5_4():
    result = parse_time_references('5.4 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_10_2():
    result = parse_time_references('10.2 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_float_days_future_30_4():
    result = parse_time_references('30.4 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 9: Future tense (from now) — minutes
# =============================================================================

def test_float_minutes_future_30_7():
    result = parse_time_references('30.7 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_45_2():
    result = parse_time_references('45.2 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_15_8():
    result = parse_time_references('15.8 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 16
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_90_3():
    result = parse_time_references('90.3 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 90
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_2_7():
    result = parse_time_references('2.7 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_60_4():
    result = parse_time_references('60.4 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 60
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_5_1():
    result = parse_time_references('5.1 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_minutes_future_10_3():
    result = parse_time_references('10.3 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 10: Future tense (from now) — hours
# =============================================================================

def test_float_hours_future_3_7():
    result = parse_time_references('3.7 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_8_2():
    result = parse_time_references('8.2 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_24_4():
    result = parse_time_references('24.4 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 24
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_6_8():
    result = parse_time_references('6.8 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_12_1():
    result = parse_time_references('12.1 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_0_9():
    result = parse_time_references('0.9 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_2_3():
    result = parse_time_references('2.3 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_hours_future_18_7():
    result = parse_time_references('18.7 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 19
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 11: Future tense (from now) — weeks
# =============================================================================

def test_float_weeks_future_1_4():
    result = parse_time_references('1.4 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_float_weeks_future_2_8():
    result = parse_time_references('2.8 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_float_weeks_future_4_2():
    result = parse_time_references('4.2 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_float_weeks_future_3_6():
    result = parse_time_references('3.6 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_float_weeks_future_0_7():
    result = parse_time_references('0.7 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


# =============================================================================
# Section 12: Future tense (from now) — months
# =============================================================================

def test_float_months_future_1_4():
    result = parse_time_references('1.4 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_float_months_future_4_8():
    result = parse_time_references('4.8 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_float_months_future_2_6():
    result = parse_time_references('2.6 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_float_months_future_3_3():
    result = parse_time_references('3.3 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_float_months_future_11_8():
    result = parse_time_references('11.8 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


# =============================================================================
# Section 13: Future tense (from now) — years
# =============================================================================

def test_float_years_future_1_4():
    result = parse_time_references('1.4 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_years_future_2_7():
    result = parse_time_references('2.7 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_years_future_3_8():
    result = parse_time_references('3.8 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_years_future_0_6():
    result = parse_time_references('0.6 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_years_future_5_2():
    result = parse_time_references('5.2 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


# =============================================================================
# Section 14: Future tense (from now) — seconds
# =============================================================================

def test_float_seconds_future_10_3():
    result = parse_time_references('10.3 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_seconds_future_30_7():
    result = parse_time_references('30.7 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_seconds_future_45_2():
    result = parse_time_references('45.2 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_seconds_future_2_4():
    result = parse_time_references('2.4 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_seconds_future_59_8():
    result = parse_time_references('59.8 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 60
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


# =============================================================================
# Section 15: Rounding — round-down cases (decimal < .5)
# These must produce floor(x), not ceil(x).
# =============================================================================

def test_rounding_down_2_1():
    result = parse_time_references('2.1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_rounding_down_5_3():
    result = parse_time_references('5.3 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 5


def test_rounding_down_10_1():
    result = parse_time_references('10.1 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 10


def test_rounding_down_3_4():
    result = parse_time_references('3.4 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 3


def test_rounding_down_1_4_months():
    result = parse_time_references('1.4 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 1


def test_rounding_down_7_2():
    result = parse_time_references('7.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7


def test_rounding_down_4_4_years():
    result = parse_time_references('4.4 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 4


def test_rounding_down_3_1():
    result = parse_time_references('3.1 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 3


def test_rounding_down_8_2_hours():
    result = parse_time_references('8.2 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 8


def test_rounding_down_20_3():
    result = parse_time_references('20.3 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 20


def test_rounding_down_6_1():
    result = parse_time_references('6.1 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 6


def test_rounding_down_9_4():
    result = parse_time_references('9.4 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 9


def test_rounding_down_11_2():
    result = parse_time_references('11.2 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 11


# =============================================================================
# Section 16: Rounding — round-up cases (decimal > .5)
# =============================================================================

def test_rounding_up_2_6():
    result = parse_time_references('2.6 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 3


def test_rounding_up_5_8():
    result = parse_time_references('5.8 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 6


def test_rounding_up_10_9():
    result = parse_time_references('10.9 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 11


def test_rounding_up_3_6():
    result = parse_time_references('3.6 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 4


def test_rounding_up_1_7():
    result = parse_time_references('1.7 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_rounding_up_4_8():
    result = parse_time_references('4.8 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 5


def test_rounding_up_8_9():
    result = parse_time_references('8.9 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 9


def test_rounding_up_22_6():
    result = parse_time_references('22.6 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 23


def test_rounding_up_3_8():
    result = parse_time_references('3.8 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 4


def test_rounding_up_11_9():
    result = parse_time_references('11.9 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 12


def test_rounding_up_6_7():
    result = parse_time_references('6.7 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7


def test_rounding_up_0_7_years():
    result = parse_time_references('0.7 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1


def test_rounding_up_14_8():
    result = parse_time_references('14.8 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 15


# =============================================================================
# Section 17: Multi-decimal precision (3+ decimal places)
# =============================================================================

def test_multi_decimal_22_355_hours():
    result = parse_time_references('22.355 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 22
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_multi_decimal_5_11553_years():
    result = parse_time_references('5.11553 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_multi_decimal_7_123_days():
    result = parse_time_references('7.123 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_multi_decimal_3_456_weeks():
    result = parse_time_references('3.456 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_multi_decimal_2_789_months():
    result = parse_time_references('2.789 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_multi_decimal_15_001_minutes():
    result = parse_time_references('15.001 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_multi_decimal_1_234567_years():
    result = parse_time_references('1.234567 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_multi_decimal_100_567_days():
    result = parse_time_references('100.567 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 101
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_multi_decimal_4_999_hours():
    result = parse_time_references('4.999 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_multi_decimal_0_999_days():
    result = parse_time_references('0.999 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 18: Cardinality type must be int (not float)
# =============================================================================

def test_cardinality_type_is_int_days():
    result = parse_time_references('7.2 days ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_minutes():
    result = parse_time_references('58.4 minutes ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_hours():
    result = parse_time_references('8.3 hours ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_weeks():
    result = parse_time_references('2.3 weeks ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_months():
    result = parse_time_references('4.8 months ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_years():
    result = parse_time_references('5.11553 years ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_seconds():
    result = parse_time_references('30.7 seconds ago')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_is_int_future():
    result = parse_time_references('7.8 days from now')
    assert isinstance(result[0].cardinality, int)


# =============================================================================
# Section 19: API coverage — extract_past_references, extract_future_references,
#              has_temporal_info, resolve_to_timedelta, parse_dates
# =============================================================================

def test_extract_past_7_2_days():
    result = extract_past_references('7.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].tense == 'past'


def test_extract_past_4_8_months():
    result = extract_past_references('4.8 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].tense == 'past'


def test_extract_past_22_355_hours():
    result = extract_past_references('22.355 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 22
    assert result[0].tense == 'past'


def test_extract_future_not_in_past():
    result = extract_past_references('7.2 days from now')
    assert len(result) == 0


def test_extract_future_7_2_days():
    result = extract_future_references('7.2 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].tense == 'future'


def test_extract_future_3_8_weeks():
    result = extract_future_references('3.8 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].tense == 'future'


def test_extract_past_not_in_future():
    result = extract_future_references('7.2 days ago')
    assert len(result) == 0


def test_has_temporal_info_float_past():
    assert has_temporal_info('7.2 days ago') is True


def test_has_temporal_info_float_future():
    assert has_temporal_info('3.8 weeks from now') is True


def test_resolve_to_timedelta_float_past():
    deltas = resolve_to_timedelta('7.2 days ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_resolve_to_timedelta_float_future():
    deltas = resolve_to_timedelta('7.2 days from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_resolve_to_timedelta_rounded_value():
    deltas = resolve_to_timedelta('7.2 days ago')
    assert deltas[0] == timedelta(days=-7)


def test_resolve_to_timedelta_rounded_up():
    deltas = resolve_to_timedelta('7.8 days ago')
    assert deltas[0] == timedelta(days=-8)


def test_parse_dates_float_cardinality():
    result = parse_dates('7.2 days ago')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 7


def test_extract_relative_times_float():
    result = extract_relative_times('22.355 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 22
    assert result[0].frame == 'hour'


# =============================================================================
# Section 20: Sentence context — float in longer text
# =============================================================================

def test_sentence_float_days_ago():
    result = parse_time_references('show me records from 7.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_sentence_float_hours_ago():
    result = parse_time_references('email received 8.3 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'


def test_sentence_float_months_ago():
    result = parse_time_references('account created 4.8 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'


def test_sentence_float_years_ago():
    result = parse_time_references('joined 5.11553 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'


def test_sentence_float_from_now():
    result = parse_time_references('deadline is 3.8 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_sentence_float_minutes_ago():
    result = parse_time_references('last login 58.4 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 58
    assert result[0].frame == 'minute'


def test_sentence_float_weeks_ago():
    result = parse_time_references('project started 2.3 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'


def test_sentence_float_seconds_ago():
    result = parse_time_references('ping received 30.7 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'second'


# =============================================================================
# Section 21: Abbreviated units with floats
# =============================================================================

def test_float_abbrev_hrs_past():
    result = parse_time_references('8.3 hrs ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_abbrev_mins_past():
    result = parse_time_references('58.4 mins ago')
    assert len(result) == 1
    assert result[0].cardinality == 58
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_abbrev_secs_past():
    result = parse_time_references('30.7 secs ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_abbrev_wks_past():
    result = parse_time_references('2.3 wks ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_abbrev_yrs_past():
    result = parse_time_references('5.11553 yrs ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_abbrev_mos_past():
    result = parse_time_references('4.8 mos ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_abbrev_hrs_future():
    result = parse_time_references('8.2 hrs from now')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_abbrev_mins_future():
    result = parse_time_references('45.2 mins from now')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_abbrev_wks_future():
    result = parse_time_references('3.6 wks from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_float_abbrev_yrs_future():
    result = parse_time_references('2.7 yrs from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_abbrev_hr_singular_past():
    result = parse_time_references('2.4 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_abbrev_min_singular_past():
    result = parse_time_references('10.1 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


# =============================================================================
# Section 22: Timedelta sign validation
# Past → negative timedelta, Future → positive timedelta
# =============================================================================

def test_timedelta_float_past_is_negative():
    deltas = resolve_to_timedelta('7.2 days ago')
    assert deltas[0].total_seconds() < 0


def test_timedelta_float_future_is_positive():
    deltas = resolve_to_timedelta('7.2 days from now')
    assert deltas[0].total_seconds() > 0


def test_timedelta_float_hours_past_is_negative():
    deltas = resolve_to_timedelta('8.3 hours ago')
    assert deltas[0].total_seconds() < 0


def test_timedelta_float_months_past_is_negative():
    deltas = resolve_to_timedelta('4.8 months ago')
    assert deltas[0].total_seconds() < 0


def test_timedelta_float_years_past_value():
    deltas = resolve_to_timedelta('5.11553 years ago')
    assert deltas[0].total_seconds() < 0


def test_timedelta_float_weeks_future_is_positive():
    deltas = resolve_to_timedelta('3.8 weeks from now')
    assert deltas[0].total_seconds() > 0


def test_timedelta_float_minutes_past_value():
    deltas = resolve_to_timedelta('58.4 minutes ago')
    assert deltas[0] == timedelta(minutes=-58)


def test_timedelta_float_hours_rounded_up():
    deltas = resolve_to_timedelta('3.7 hours ago')
    assert deltas[0] == timedelta(hours=-4)


# =============================================================================
# Section 23: Regression — integer cardinalities must still work unchanged
# =============================================================================

def test_regression_integer_days_5():
    result = parse_time_references('5 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_regression_integer_hours_3():
    result = parse_time_references('3 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_integer_weeks_2():
    result = parse_time_references('2 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_regression_integer_months_1():
    result = parse_time_references('1 month ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_regression_integer_years_10():
    result = parse_time_references('10 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_regression_integer_future_7():
    result = parse_time_references('7 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_regression_integer_minutes_30():
    result = parse_time_references('30 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_integer_seconds_45():
    result = parse_time_references('45 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_regression_last_week():
    result = parse_time_references('last week')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_regression_cardinality_type_integer_input():
    result = parse_time_references('5 days ago')
    assert isinstance(result[0].cardinality, int)
    assert result[0].cardinality == 5


# =============================================================================
# Section 24: Capitalization robustness — float inputs with mixed case
# =============================================================================

def test_capitalized_float_days_ago():
    result = parse_time_references('7.2 Days Ago')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_capitalized_float_hours_ago():
    result = parse_time_references('8.3 Hours Ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_capitalized_float_months_ago():
    result = parse_time_references('4.8 Months Ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_capitalized_float_weeks_from_now():
    result = parse_time_references('3.7 Weeks From Now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_capitalized_float_years_ago():
    result = parse_time_references('5.11553 Years Ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_uppercase_float_days_ago():
    result = parse_time_references('7.2 DAYS AGO')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 25: Singular abbreviated units with floats (hr, min, sec, wk, yr, mo)
# =============================================================================

def test_float_secs_plural_past():
    result = parse_time_references('30.7 secs ago')
    assert len(result) == 1
    assert result[0].cardinality == 31
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_yrs_plural_past():
    result = parse_time_references('5.11553 yrs ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_mos_plural_past():
    result = parse_time_references('4.8 mos ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_wks_plural_past():
    result = parse_time_references('2.3 wks ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_hr_singular_future():
    result = parse_time_references('3.7 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 4
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_secs_plural_future():
    result = parse_time_references('45.2 secs from now')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_yrs_plural_future():
    result = parse_time_references('2.7 yrs from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


# =============================================================================
# Section 26: Additional varied cardinalities — past tense
# =============================================================================

def test_float_days_past_50_3():
    result = parse_time_references('50.3 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 50
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_hours_past_48_7():
    result = parse_time_references('48.7 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 49
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_float_minutes_past_180_4():
    result = parse_time_references('180.4 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 180
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_float_weeks_past_6_3():
    result = parse_time_references('6.3 weeks ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_float_months_past_7_7():
    result = parse_time_references('7.7 months ago')
    assert len(result) == 1
    assert result[0].cardinality == 8
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_float_years_past_10_2():
    result = parse_time_references('10.2 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'year'
    assert result[0].tense == 'past'


def test_float_seconds_past_90_3():
    result = parse_time_references('90.3 seconds ago')
    assert len(result) == 1
    assert result[0].cardinality == 90
    assert result[0].frame == 'second'
    assert result[0].tense == 'past'


def test_float_days_past_200_8():
    result = parse_time_references('200.8 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 201
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_hours_future_36_2():
    result = parse_time_references('36.2 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 36
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_float_minutes_future_1_4():
    result = parse_time_references('1.4 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_float_seconds_future_0_9():
    result = parse_time_references('0.9 seconds from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'second'
    assert result[0].tense == 'future'


def test_float_months_future_6_8():
    result = parse_time_references('6.8 months from now')
    assert len(result) == 1
    assert result[0].cardinality == 7
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_float_years_future_10_3():
    result = parse_time_references('10.3 years from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_float_weeks_future_8_7():
    result = parse_time_references('8.7 weeks from now')
    assert len(result) == 1
    assert result[0].cardinality == 9
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


# =============================================================================
# Section 27: has_temporal_info — variety of float inputs
# =============================================================================

def test_has_temporal_info_float_minutes_ago():
    assert has_temporal_info('58.4 minutes ago') is True


def test_has_temporal_info_float_years_ago():
    assert has_temporal_info('5.11553 years ago') is True


def test_has_temporal_info_float_hours_from_now():
    assert has_temporal_info('8.3 hours from now') is True


def test_has_temporal_info_float_months_ago():
    assert has_temporal_info('4.8 months ago') is True


def test_has_temporal_info_float_weeks_from_now():
    assert has_temporal_info('2.3 weeks from now') is True


def test_has_temporal_info_float_seconds_ago():
    assert has_temporal_info('30.7 seconds ago') is True


def test_has_temporal_info_float_days_from_now():
    assert has_temporal_info('14.2 days from now') is True


def test_has_temporal_info_no_float_match():
    assert has_temporal_info('7.2 is a decimal number') is False


def test_float_days_past_4_6():
    result = parse_time_references('4.6 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_float_hours_past_16_8():
    result = parse_time_references('16.8 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 17
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'
