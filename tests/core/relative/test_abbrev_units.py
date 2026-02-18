#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #9: abbreviated unit forms for N > 1.

parsedatetime accepts '5 min ago', '5 hr from now', '5 hour ago', etc.
fast-parse-time should do the same.

Covered abbreviations:
    - 'min'  → minute (singular abbrev, N > 1 and N == 1)
    - 'mins' → minutes (plural abbrev, should already work — regression)
    - 'hr'   → hour (singular abbrev, N > 1 and N == 1)
    - 'hrs'  → hours (plural abbrev, should already work — regression)
    - 'hour' → hours (singular unit used with N > 1, e.g. '5 hour ago')

Covered tenses:
    - Past:   'ago', 'before now', 'back', 'prior'
    - Future: 'from now', 'in N <unit>'

Covered cardinalities:
    - N == 1 regression (must still work after normalization)
    - N > 1: 2, 3, 5, 10, 15, 20, 30, 45

Covered APIs:
    - parse_time_references
    - extract_relative_times
    - extract_past_references
    - extract_future_references
    - has_temporal_info
    - resolve_to_timedelta
    - parse_dates

Related GitHub Issue:
    #9 - Gap: abbreviated unit forms not recognized (min, hr, singular hour/day)
    https://github.com/craigtrim/fast-parse-time/issues/9
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
# Section 1: 'min' abbreviated form — past tense (ago)
# =============================================================================

def test_min_past_2_ago():
    result = parse_time_references('2 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_3_ago():
    result = parse_time_references('3 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_5_ago():
    result = parse_time_references('5 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_10_ago():
    result = parse_time_references('10 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_15_ago():
    result = parse_time_references('15 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_20_ago():
    result = parse_time_references('20 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 20
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_30_ago():
    result = parse_time_references('30 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_past_45_ago():
    result = parse_time_references('45 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


# =============================================================================
# Section 2: 'min' abbreviated form — future tense (from now)
# =============================================================================

def test_min_future_2_from_now():
    result = parse_time_references('2 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_5_from_now():
    result = parse_time_references('5 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_10_from_now():
    result = parse_time_references('10 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_15_from_now():
    result = parse_time_references('15 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_30_from_now():
    result = parse_time_references('30 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_45_from_now():
    result = parse_time_references('45 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 3: 'min' abbreviated form — future tense (in N min)
# =============================================================================

def test_min_future_in_5():
    result = parse_time_references('in 5 min')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_in_10():
    result = parse_time_references('in 10 min')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_in_15():
    result = parse_time_references('in 15 min')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_min_future_in_30():
    result = parse_time_references('in 30 min')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 4: 'hr' abbreviated form — past tense (ago)
# =============================================================================

def test_hr_past_2_ago():
    result = parse_time_references('2 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_past_3_ago():
    result = parse_time_references('3 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_past_5_ago():
    result = parse_time_references('5 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_past_10_ago():
    result = parse_time_references('10 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_past_12_ago():
    result = parse_time_references('12 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_past_24_ago():
    result = parse_time_references('24 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 24
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


# =============================================================================
# Section 5: 'hr' abbreviated form — future tense (from now)
# =============================================================================

def test_hr_future_2_from_now():
    result = parse_time_references('2 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_3_from_now():
    result = parse_time_references('3 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_5_from_now():
    result = parse_time_references('5 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_12_from_now():
    result = parse_time_references('12 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_24_from_now():
    result = parse_time_references('24 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 24
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 6: 'hr' abbreviated form — future tense (in N hr)
# =============================================================================

def test_hr_future_in_2():
    result = parse_time_references('in 2 hr')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_in_5():
    result = parse_time_references('in 5 hr')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hr_future_in_12():
    result = parse_time_references('in 12 hr')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 7: 'hour' singular for N > 1 — past tense
# =============================================================================

def test_hour_singular_past_2_ago():
    result = parse_time_references('2 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_singular_past_3_ago():
    result = parse_time_references('3 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_singular_past_5_ago():
    result = parse_time_references('5 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_singular_past_10_ago():
    result = parse_time_references('10 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_singular_past_24_ago():
    result = parse_time_references('24 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 24
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


# =============================================================================
# Section 8: 'hour' singular for N > 1 — future tense
# =============================================================================

def test_hour_singular_future_2_from_now():
    result = parse_time_references('2 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hour_singular_future_3_from_now():
    result = parse_time_references('3 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hour_singular_future_5_from_now():
    result = parse_time_references('5 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hour_singular_future_10_from_now():
    result = parse_time_references('10 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_hour_singular_future_in_5():
    result = parse_time_references('in 5 hour')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 9: Regression — cardinality 1 with abbreviated units still works
# (normalization must NOT fire for N == 1)
# =============================================================================

def test_regression_1_min_ago():
    """Cardinality-1 'min' must still resolve after plural normalization is added."""
    result = parse_time_references('1 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_1_min_from_now():
    result = parse_time_references('1 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_regression_1_hr_ago():
    result = parse_time_references('1 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_1_hr_from_now():
    result = parse_time_references('1 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_regression_1_hour_ago():
    """Cardinality-1 'hour' singular must still resolve."""
    result = parse_time_references('1 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_1_hour_from_now():
    result = parse_time_references('1 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 10: Past-tense aliases — 'before now', 'back', 'prior'
# =============================================================================

def test_min_before_now_5():
    result = parse_time_references('5 min before now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_back_10():
    result = parse_time_references('10 min back')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_prior_15():
    result = parse_time_references('15 min prior')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_hr_before_now_3():
    result = parse_time_references('3 hr before now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_back_5():
    result = parse_time_references('5 hr back')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hr_prior_2():
    result = parse_time_references('2 hr prior')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_before_now_5():
    result = parse_time_references('5 hour before now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_back_3():
    result = parse_time_references('3 hour back')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_prior_2():
    result = parse_time_references('2 hour prior')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


# =============================================================================
# Section 11: Sentence context — abbreviated units embedded in prose
# =============================================================================

def test_context_sent_5_min_ago():
    result = parse_time_references('message sent 5 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_context_show_data_from_10_min_ago():
    result = parse_time_references('show data from 10 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_context_meeting_in_30_min():
    result = parse_time_references('meeting starts in 30 min')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_context_alarm_in_5_min():
    result = parse_time_references('set alarm in 5 min')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_context_event_3_hr_ago():
    result = parse_time_references('event occurred 3 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_context_flight_in_2_hr():
    result = parse_time_references('flight departs in 2 hr')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_context_report_5_hour_ago():
    result = parse_time_references('filed report 5 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_context_meeting_3_hour_from_now():
    result = parse_time_references('meeting 3 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_context_reminder_set_20_min_ago():
    result = parse_time_references('reminder was set 20 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 20
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_context_call_back_in_5_min():
    result = parse_time_references('I will call back in 5 min')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 12: Spelled-out numbers with abbreviated units
# =============================================================================

def test_word_number_five_min_ago():
    result = parse_time_references('five min ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_word_number_ten_min_from_now():
    result = parse_time_references('ten min from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_word_number_three_hr_ago():
    result = parse_time_references('three hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_word_number_five_hr_from_now():
    result = parse_time_references('five hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_word_number_two_hour_ago():
    result = parse_time_references('two hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_word_number_three_hour_from_now():
    result = parse_time_references('three hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_word_number_fifteen_min_ago():
    result = parse_time_references('fifteen min ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_word_number_twenty_min_from_now():
    result = parse_time_references('twenty min from now')
    assert len(result) == 1
    assert result[0].cardinality == 20
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_word_number_thirty_min_ago():
    result = parse_time_references('thirty min ago')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_word_number_twelve_hr_from_now():
    result = parse_time_references('twelve hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 12
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 13: Capitalization variants
# =============================================================================

def test_capitalized_Min_past():
    result = parse_time_references('5 Min ago')
    assert len(result) == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_uppercase_MIN_past():
    result = parse_time_references('5 MIN ago')
    assert len(result) == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_capitalized_Hr_past():
    result = parse_time_references('3 Hr ago')
    assert len(result) == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_uppercase_HR_past():
    result = parse_time_references('3 HR ago')
    assert len(result) == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_capitalized_Hour_past():
    result = parse_time_references('5 Hour ago')
    assert len(result) == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_titlecase_Hr_from_now():
    result = parse_time_references('5 Hr from now')
    assert len(result) == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_uppercase_MIN_from_now():
    result = parse_time_references('10 MIN from now')
    assert len(result) == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_capitalized_sentence_5_Min_from_now():
    result = parse_time_references('Alarm in 5 Min from now')
    assert len(result) == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 14: has_temporal_info — abbreviated units detected
# =============================================================================

def test_has_temporal_info_5_min_ago():
    assert has_temporal_info('5 min ago') is True


def test_has_temporal_info_in_5_min():
    assert has_temporal_info('in 5 min') is True


def test_has_temporal_info_2_hr_ago():
    assert has_temporal_info('2 hr ago') is True


def test_has_temporal_info_5_hr_from_now():
    assert has_temporal_info('5 hr from now') is True


def test_has_temporal_info_3_hour_ago():
    assert has_temporal_info('3 hour ago') is True


def test_has_temporal_info_5_hour_from_now():
    assert has_temporal_info('5 hour from now') is True


def test_has_temporal_info_in_12_hr():
    assert has_temporal_info('in 12 hr') is True


def test_has_temporal_info_no_abbrev_unit():
    assert has_temporal_info('just checking') is False


# =============================================================================
# Section 15: resolve_to_timedelta — sign validation
# (past = negative, future = positive)
# =============================================================================

def test_timedelta_5_min_ago_is_negative():
    deltas = resolve_to_timedelta('5 min ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_10_min_ago_is_negative():
    deltas = resolve_to_timedelta('10 min ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_5_min_from_now_is_positive():
    deltas = resolve_to_timedelta('5 min from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_10_min_from_now_is_positive():
    deltas = resolve_to_timedelta('10 min from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_3_hr_ago_is_negative():
    deltas = resolve_to_timedelta('3 hr ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_5_hr_from_now_is_positive():
    deltas = resolve_to_timedelta('5 hr from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_5_hour_ago_is_negative():
    deltas = resolve_to_timedelta('5 hour ago')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_3_hour_from_now_is_positive():
    deltas = resolve_to_timedelta('3 hour from now')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_30_min_ago_exact():
    deltas = resolve_to_timedelta('30 min ago')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(minutes=-30)


def test_timedelta_30_min_from_now_exact():
    deltas = resolve_to_timedelta('30 min from now')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(minutes=30)


def test_timedelta_2_hr_ago_exact():
    deltas = resolve_to_timedelta('2 hr ago')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(hours=-2)


def test_timedelta_2_hr_from_now_exact():
    deltas = resolve_to_timedelta('2 hr from now')
    assert len(deltas) == 1
    assert deltas[0] == timedelta(hours=2)


# =============================================================================
# Section 16: extract_past_references / extract_future_references
# =============================================================================

def test_extract_past_5_min_ago():
    result = extract_past_references('5 min ago')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].frame == 'minute'
    assert result[0].cardinality == 5


def test_extract_past_10_min_ago():
    result = extract_past_references('10 min ago')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].cardinality == 10


def test_extract_past_3_hr_ago():
    result = extract_past_references('3 hr ago')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].frame == 'hour'
    assert result[0].cardinality == 3


def test_extract_past_5_hour_ago():
    result = extract_past_references('5 hour ago')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].frame == 'hour'


def test_extract_future_5_min_from_now():
    result = extract_future_references('5 min from now')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'minute'
    assert result[0].cardinality == 5


def test_extract_future_in_10_min():
    result = extract_future_references('in 10 min')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'minute'


def test_extract_future_5_hr_from_now():
    result = extract_future_references('5 hr from now')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'hour'
    assert result[0].cardinality == 5


def test_extract_future_3_hour_from_now():
    result = extract_future_references('3 hour from now')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'hour'


def test_extract_future_returns_empty_for_past_min():
    """Abbreviated past form must not appear in future bucket."""
    result = extract_future_references('5 min ago')
    assert len(result) == 0


def test_extract_past_returns_empty_for_future_min():
    """Abbreviated future form must not appear in past bucket."""
    result = extract_past_references('5 min from now')
    assert len(result) == 0


def test_extract_future_returns_empty_for_past_hr():
    result = extract_future_references('3 hr ago')
    assert len(result) == 0


def test_extract_past_returns_empty_for_future_hr():
    result = extract_past_references('3 hr from now')
    assert len(result) == 0


# =============================================================================
# Section 17: parse_dates integrated API
# =============================================================================

def test_parse_dates_5_min_ago():
    result = parse_dates('alert from 5 min ago')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 5
    assert result.relative_times[0].frame == 'minute'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_10_min_from_now():
    result = parse_dates('reminder in 10 min from now')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 10
    assert result.relative_times[0].frame == 'minute'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_3_hr_ago():
    result = parse_dates('data logged 3 hr ago')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 3
    assert result.relative_times[0].frame == 'hour'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_5_hr_from_now():
    result = parse_dates('flight in 5 hr from now')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 5
    assert result.relative_times[0].frame == 'hour'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_5_hour_ago():
    result = parse_dates('system restarted 5 hour ago')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 5
    assert result.relative_times[0].frame == 'hour'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_3_hour_from_now():
    result = parse_dates('call scheduled 3 hour from now')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 3
    assert result.relative_times[0].frame == 'hour'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_in_30_min():
    result = parse_dates('departs in 30 min')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 30
    assert result.relative_times[0].frame == 'minute'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_20_min_ago():
    result = parse_dates('call ended 20 min ago')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 20
    assert result.relative_times[0].frame == 'minute'
    assert result.relative_times[0].tense == 'past'


# =============================================================================
# Section 18: Regression — full plural forms still work after adding abbrev support
# (normalization must not double-convert already-correct forms)
# =============================================================================

def test_regression_plural_5_mins_ago():
    result = parse_time_references('5 mins ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_plural_5_minutes_ago():
    result = parse_time_references('5 minutes ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_regression_plural_5_hrs_ago():
    result = parse_time_references('5 hrs ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_plural_5_hours_ago():
    result = parse_time_references('5 hours ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_regression_plural_5_minutes_from_now():
    result = parse_time_references('5 minutes from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_regression_plural_5_hours_from_now():
    result = parse_time_references('5 hours from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_regression_plural_10_mins_from_now():
    result = parse_time_references('10 mins from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_regression_plural_10_hrs_from_now():
    result = parse_time_references('10 hrs from now')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 19: extract_relative_times low-level API with abbrev forms
# =============================================================================

def test_extract_relative_times_5_min_ago():
    result = extract_relative_times('5 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_extract_relative_times_in_10_min():
    result = extract_relative_times('in 10 min')
    assert len(result) == 1
    assert result[0].cardinality == 10
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_extract_relative_times_3_hr_ago():
    result = extract_relative_times('3 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_extract_relative_times_5_hr_from_now():
    result = extract_relative_times('5 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_extract_relative_times_5_hour_ago():
    result = extract_relative_times('5 hour ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_extract_relative_times_3_hour_from_now():
    result = extract_relative_times('3 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


# =============================================================================
# Section 20: Indefinite article 'an' with abbreviated units
# (e.g. 'an hr ago', 'an hr from now' — 'an' resolves to cardinality 1)
# =============================================================================

def test_an_hr_ago():
    result = parse_time_references('an hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_an_hr_from_now():
    result = parse_time_references('an hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_an_hr_before_now():
    result = parse_time_references('an hr before now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_an_min_ago():
    result = parse_time_references('a min ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_an_min_from_now():
    result = parse_time_references('a min from now')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


# =============================================================================
# Section 21: Larger cardinalities — spot-check above 24
# =============================================================================

def test_min_past_large_45_ago():
    result = parse_time_references('45 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 45
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_min_future_large_50_from_now():
    result = parse_time_references('50 min from now')
    assert len(result) == 1
    assert result[0].cardinality == 50
    assert result[0].frame == 'minute'
    assert result[0].tense == 'future'


def test_hr_past_large_36_ago():
    result = parse_time_references('36 hr ago')
    assert len(result) == 1
    assert result[0].cardinality == 36
    assert result[0].frame == 'hour'
    assert result[0].tense == 'past'


def test_hour_singular_large_48_from_now():
    result = parse_time_references('48 hour from now')
    assert len(result) == 1
    assert result[0].cardinality == 48
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'


def test_min_past_large_59_ago():
    result = parse_time_references('59 min ago')
    assert len(result) == 1
    assert result[0].cardinality == 59
    assert result[0].frame == 'minute'
    assert result[0].tense == 'past'


def test_hr_future_large_72_from_now():
    result = parse_time_references('72 hr from now')
    assert len(result) == 1
    assert result[0].cardinality == 72
    assert result[0].frame == 'hour'
    assert result[0].tense == 'future'
