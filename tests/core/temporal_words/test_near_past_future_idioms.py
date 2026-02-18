#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #18: Near-past/near-future idioms not supported.

Covers fixed-cardinality idiomatic expressions for days near the present:

    Near-past (2 days ago):
        - 'the day before yesterday'
        - 'day before yesterday'

    Near-future (2 days from now):
        - 'the day after tomorrow'   (bug fix: currently returns cardinality=1)
        - 'day after tomorrow'       (bug fix: currently returns cardinality=1)
        - 'overmorrow'               (archaic single-token form)

    Present-anchored (0 days, present tense):
        - 'till date'
        - 'to date'

Already working — regression coverage only:
    - 'yesterday', 'today', 'tomorrow'

Out of scope:
    - 'the other day' (no fixed cardinality)
    - 'just now' (issue #16, done)
    - time-of-day qualifiers (yesterday morning, etc.)

Related GitHub Issues:
    #18 - Gap: near-past/near-future idioms not supported
    https://github.com/craigtrim/fast-parse-time/issues/18
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
# Section 1: 'the day before yesterday' — bare form
# =============================================================================

def test_the_day_before_yesterday_bare():
    result = parse_time_references('the day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_the_day_before_yesterday_cardinality():
    result = parse_time_references('the day before yesterday')
    assert result[0].cardinality == 2


def test_the_day_before_yesterday_frame():
    result = parse_time_references('the day before yesterday')
    assert result[0].frame == 'day'


def test_the_day_before_yesterday_tense():
    result = parse_time_references('the day before yesterday')
    assert result[0].tense == 'past'


def test_the_day_before_yesterday_result_count():
    result = parse_time_references('the day before yesterday')
    assert len(result) == 1


def test_the_day_before_yesterday_extract_past():
    result = extract_past_references('the day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_the_day_before_yesterday_not_in_future():
    result = extract_future_references('the day before yesterday')
    assert len(result) == 0


def test_the_day_before_yesterday_has_temporal_info():
    assert has_temporal_info('the day before yesterday') is True


def test_the_day_before_yesterday_timedelta_negative():
    deltas = resolve_to_timedelta('the day before yesterday')
    assert len(deltas) == 1
    assert deltas[0].total_seconds() < 0


def test_the_day_before_yesterday_timedelta_value():
    deltas = resolve_to_timedelta('the day before yesterday')
    assert deltas[0] == timedelta(days=-2)


def test_the_day_before_yesterday_parse_dates():
    result = parse_dates('the day before yesterday')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


def test_the_day_before_yesterday_extract_relative():
    result = extract_relative_times('the day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'


# =============================================================================
# Section 2: 'day before yesterday' (without 'the')
# =============================================================================

def test_day_before_yesterday_bare():
    result = parse_time_references('day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_day_before_yesterday_extract_past():
    result = extract_past_references('day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_day_before_yesterday_not_in_future():
    result = extract_future_references('day before yesterday')
    assert len(result) == 0


def test_day_before_yesterday_has_temporal_info():
    assert has_temporal_info('day before yesterday') is True


def test_day_before_yesterday_timedelta():
    deltas = resolve_to_timedelta('day before yesterday')
    assert deltas[0] == timedelta(days=-2)


def test_day_before_yesterday_parse_dates():
    result = parse_dates('day before yesterday')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


# =============================================================================
# Section 3: 'the day after tomorrow' — bug fix (currently returns 1, should be 2)
# =============================================================================

def test_the_day_after_tomorrow_bare():
    result = parse_time_references('the day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_the_day_after_tomorrow_cardinality():
    result = parse_time_references('the day after tomorrow')
    assert result[0].cardinality == 2


def test_the_day_after_tomorrow_tense():
    result = parse_time_references('the day after tomorrow')
    assert result[0].tense == 'future'


def test_the_day_after_tomorrow_frame():
    result = parse_time_references('the day after tomorrow')
    assert result[0].frame == 'day'


def test_the_day_after_tomorrow_extract_future():
    result = extract_future_references('the day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_the_day_after_tomorrow_not_in_past():
    result = extract_past_references('the day after tomorrow')
    assert len(result) == 0


def test_the_day_after_tomorrow_has_temporal_info():
    assert has_temporal_info('the day after tomorrow') is True


def test_the_day_after_tomorrow_timedelta_positive():
    deltas = resolve_to_timedelta('the day after tomorrow')
    assert len(deltas) == 1
    assert deltas[0].total_seconds() > 0


def test_the_day_after_tomorrow_timedelta_value():
    deltas = resolve_to_timedelta('the day after tomorrow')
    assert deltas[0] == timedelta(days=2)


def test_the_day_after_tomorrow_parse_dates():
    result = parse_dates('the day after tomorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


def test_the_day_after_tomorrow_extract_relative():
    result = extract_relative_times('the day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2


# =============================================================================
# Section 4: 'day after tomorrow' (without 'the') — bug fix
# =============================================================================

def test_day_after_tomorrow_bare():
    result = parse_time_references('day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_day_after_tomorrow_extract_future():
    result = extract_future_references('day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_day_after_tomorrow_not_in_past():
    result = extract_past_references('day after tomorrow')
    assert len(result) == 0


def test_day_after_tomorrow_has_temporal_info():
    assert has_temporal_info('day after tomorrow') is True


def test_day_after_tomorrow_timedelta():
    deltas = resolve_to_timedelta('day after tomorrow')
    assert deltas[0] == timedelta(days=2)


def test_day_after_tomorrow_parse_dates():
    result = parse_dates('day after tomorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


# =============================================================================
# Section 5: 'overmorrow' — 2 days from now
# =============================================================================

def test_overmorrow_bare():
    result = parse_time_references('overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_overmorrow_cardinality():
    result = parse_time_references('overmorrow')
    assert result[0].cardinality == 2


def test_overmorrow_tense():
    result = parse_time_references('overmorrow')
    assert result[0].tense == 'future'


def test_overmorrow_frame():
    result = parse_time_references('overmorrow')
    assert result[0].frame == 'day'


def test_overmorrow_extract_future():
    result = extract_future_references('overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_overmorrow_not_in_past():
    result = extract_past_references('overmorrow')
    assert len(result) == 0


def test_overmorrow_has_temporal_info():
    assert has_temporal_info('overmorrow') is True


def test_overmorrow_timedelta_positive():
    deltas = resolve_to_timedelta('overmorrow')
    assert deltas[0].total_seconds() > 0


def test_overmorrow_timedelta_value():
    deltas = resolve_to_timedelta('overmorrow')
    assert deltas[0] == timedelta(days=2)


def test_overmorrow_parse_dates():
    result = parse_dates('overmorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


def test_overmorrow_extract_relative():
    result = extract_relative_times('overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'day'


# =============================================================================
# Section 6: 'till date' — present-anchored
# =============================================================================

def test_till_date_bare():
    result = parse_time_references('till date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].frame == 'day'
    assert result[0].tense == 'present'


def test_till_date_cardinality():
    result = parse_time_references('till date')
    assert result[0].cardinality == 0


def test_till_date_tense():
    result = parse_time_references('till date')
    assert result[0].tense == 'present'


def test_till_date_frame():
    result = parse_time_references('till date')
    assert result[0].frame == 'day'


def test_till_date_has_temporal_info():
    assert has_temporal_info('till date') is True


def test_till_date_parse_dates():
    result = parse_dates('till date')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 0


def test_till_date_extract_relative():
    result = extract_relative_times('till date')
    assert len(result) == 1
    assert result[0].tense == 'present'


# =============================================================================
# Section 7: 'to date' — present-anchored
# =============================================================================

def test_to_date_bare():
    result = parse_time_references('to date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].frame == 'day'
    assert result[0].tense == 'present'


def test_to_date_cardinality():
    result = parse_time_references('to date')
    assert result[0].cardinality == 0


def test_to_date_tense():
    result = parse_time_references('to date')
    assert result[0].tense == 'present'


def test_to_date_frame():
    result = parse_time_references('to date')
    assert result[0].frame == 'day'


def test_to_date_has_temporal_info():
    assert has_temporal_info('to date') is True


def test_to_date_parse_dates():
    result = parse_dates('to date')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 0


def test_to_date_extract_relative():
    result = extract_relative_times('to date')
    assert len(result) == 1
    assert result[0].tense == 'present'


# =============================================================================
# Section 8: Capitalization robustness
# =============================================================================

def test_capitalized_the_day_before_yesterday():
    result = parse_time_references('The Day Before Yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_uppercase_day_before_yesterday():
    result = parse_time_references('DAY BEFORE YESTERDAY')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_capitalized_the_day_after_tomorrow():
    result = parse_time_references('The Day After Tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_uppercase_day_after_tomorrow():
    result = parse_time_references('DAY AFTER TOMORROW')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_capitalized_overmorrow():
    result = parse_time_references('Overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_uppercase_overmorrow():
    result = parse_time_references('OVERMORROW')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_capitalized_till_date():
    result = parse_time_references('Till Date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_uppercase_till_date():
    result = parse_time_references('TILL DATE')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_capitalized_to_date():
    result = parse_time_references('To Date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_uppercase_to_date():
    result = parse_time_references('TO DATE')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


# =============================================================================
# Section 9: Sentence context — expressions embedded in longer text
# =============================================================================

def test_sentence_the_day_before_yesterday():
    result = parse_time_references('email was sent the day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_sentence_day_before_yesterday():
    result = parse_time_references('report filed day before yesterday is missing')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_sentence_the_day_after_tomorrow():
    result = parse_time_references('meeting is scheduled the day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_sentence_day_after_tomorrow():
    result = parse_time_references('deadline is day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_sentence_overmorrow():
    result = parse_time_references('the package arrives overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_sentence_till_date():
    result = parse_time_references('show me results till date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_sentence_to_date():
    result = parse_time_references('revenue to date is strong')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_sentence_till_date_business():
    result = parse_time_references('sales performance till date exceeds targets')
    assert len(result) == 1
    assert result[0].tense == 'present'


def test_sentence_to_date_business():
    result = parse_time_references('total orders to date')
    assert len(result) == 1
    assert result[0].tense == 'present'


def test_sentence_the_day_before_yesterday_prefix():
    result = parse_time_references('from the day before yesterday until now')
    assert len(result) >= 1
    past_results = [r for r in result if r.tense == 'past' and r.cardinality == 2]
    assert len(past_results) == 1


def test_sentence_overmorrow_context():
    result = parse_time_references('submit your report by overmorrow at the latest')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


# =============================================================================
# Section 10: Timedelta sign and value validation
# =============================================================================

def test_timedelta_the_day_before_yesterday_is_negative():
    deltas = resolve_to_timedelta('the day before yesterday')
    assert deltas[0].total_seconds() < 0


def test_timedelta_day_before_yesterday_is_negative():
    deltas = resolve_to_timedelta('day before yesterday')
    assert deltas[0].total_seconds() < 0


def test_timedelta_the_day_after_tomorrow_is_positive():
    deltas = resolve_to_timedelta('the day after tomorrow')
    assert deltas[0].total_seconds() > 0


def test_timedelta_day_after_tomorrow_is_positive():
    deltas = resolve_to_timedelta('day after tomorrow')
    assert deltas[0].total_seconds() > 0


def test_timedelta_overmorrow_is_positive():
    deltas = resolve_to_timedelta('overmorrow')
    assert deltas[0].total_seconds() > 0


def test_timedelta_the_day_before_yesterday_exact():
    deltas = resolve_to_timedelta('the day before yesterday')
    assert deltas[0] == timedelta(days=-2)


def test_timedelta_day_before_yesterday_exact():
    deltas = resolve_to_timedelta('day before yesterday')
    assert deltas[0] == timedelta(days=-2)


def test_timedelta_the_day_after_tomorrow_exact():
    deltas = resolve_to_timedelta('the day after tomorrow')
    assert deltas[0] == timedelta(days=2)


def test_timedelta_day_after_tomorrow_exact():
    deltas = resolve_to_timedelta('day after tomorrow')
    assert deltas[0] == timedelta(days=2)


def test_timedelta_overmorrow_exact():
    deltas = resolve_to_timedelta('overmorrow')
    assert deltas[0] == timedelta(days=2)


# =============================================================================
# Section 11: Tense bucket isolation
# =============================================================================

def test_day_before_yesterday_only_in_past():
    past = extract_past_references('the day before yesterday')
    future = extract_future_references('the day before yesterday')
    assert len(past) == 1
    assert len(future) == 0


def test_day_after_tomorrow_only_in_future():
    past = extract_past_references('the day after tomorrow')
    future = extract_future_references('the day after tomorrow')
    assert len(past) == 0
    assert len(future) == 1


def test_overmorrow_only_in_future():
    past = extract_past_references('overmorrow')
    future = extract_future_references('overmorrow')
    assert len(past) == 0
    assert len(future) == 1


def test_till_date_not_in_past():
    result = extract_past_references('till date')
    assert len(result) == 0


def test_till_date_not_in_future():
    result = extract_future_references('till date')
    assert len(result) == 0


def test_to_date_not_in_past():
    result = extract_past_references('to date')
    assert len(result) == 0


def test_to_date_not_in_future():
    result = extract_future_references('to date')
    assert len(result) == 0


# =============================================================================
# Section 12: Symmetry — near-past and near-future are 2 days apart
# =============================================================================

def test_past_future_symmetry_cardinality():
    past = parse_time_references('the day before yesterday')
    future = parse_time_references('the day after tomorrow')
    assert past[0].cardinality == future[0].cardinality == 2


def test_past_future_symmetry_frame():
    past = parse_time_references('the day before yesterday')
    future = parse_time_references('the day after tomorrow')
    assert past[0].frame == future[0].frame == 'day'


def test_past_future_timedelta_magnitude():
    past_delta = resolve_to_timedelta('the day before yesterday')[0]
    future_delta = resolve_to_timedelta('the day after tomorrow')[0]
    assert abs(past_delta) == abs(future_delta)


def test_overmorrow_matches_day_after_tomorrow():
    r1 = parse_time_references('overmorrow')
    r2 = parse_time_references('the day after tomorrow')
    assert r1[0].cardinality == r2[0].cardinality
    assert r1[0].frame == r2[0].frame
    assert r1[0].tense == r2[0].tense


def test_till_date_matches_to_date():
    r1 = parse_time_references('till date')
    r2 = parse_time_references('to date')
    assert r1[0].cardinality == r2[0].cardinality
    assert r1[0].frame == r2[0].frame
    assert r1[0].tense == r2[0].tense


# =============================================================================
# Section 13: Regression — existing near-present terms still work
# =============================================================================

def test_regression_yesterday():
    result = parse_time_references('yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_regression_today():
    result = parse_time_references('today')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].frame == 'day'
    assert result[0].tense == 'present'


def test_regression_tomorrow():
    result = parse_time_references('tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_regression_yesterday_timedelta():
    deltas = resolve_to_timedelta('yesterday')
    assert deltas[0] == timedelta(days=-1)


def test_regression_tomorrow_timedelta():
    deltas = resolve_to_timedelta('tomorrow')
    assert deltas[0] == timedelta(days=1)


def test_regression_yesterday_extract_past():
    result = extract_past_references('yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 1


def test_regression_tomorrow_extract_future():
    result = extract_future_references('tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 1


def test_regression_days_ago_unaffected():
    result = parse_time_references('5 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].tense == 'past'


def test_regression_days_from_now_unaffected():
    result = parse_time_references('3 days from now')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].tense == 'future'


def test_regression_last_week_unaffected():
    result = parse_time_references('last week')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


# =============================================================================
# Section 14: has_temporal_info — full coverage
# =============================================================================

def test_has_temporal_info_the_day_before_yesterday():
    assert has_temporal_info('the day before yesterday') is True


def test_has_temporal_info_day_before_yesterday():
    assert has_temporal_info('day before yesterday') is True


def test_has_temporal_info_the_day_after_tomorrow():
    assert has_temporal_info('the day after tomorrow') is True


def test_has_temporal_info_day_after_tomorrow():
    assert has_temporal_info('day after tomorrow') is True


def test_has_temporal_info_overmorrow():
    assert has_temporal_info('overmorrow') is True


def test_has_temporal_info_till_date():
    assert has_temporal_info('till date') is True


def test_has_temporal_info_to_date():
    assert has_temporal_info('to date') is True


def test_has_temporal_info_in_sentence_day_before_yesterday():
    assert has_temporal_info('it happened the day before yesterday') is True


def test_has_temporal_info_in_sentence_overmorrow():
    assert has_temporal_info('deliver it overmorrow') is True


def test_has_temporal_info_in_sentence_till_date():
    assert has_temporal_info('figures till date look good') is True


# =============================================================================
# Section 15: parse_dates API coverage
# =============================================================================

def test_parse_dates_the_day_before_yesterday():
    result = parse_dates('the day before yesterday')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_day_before_yesterday():
    result = parse_dates('day before yesterday')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


def test_parse_dates_the_day_after_tomorrow():
    result = parse_dates('the day after tomorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_day_after_tomorrow():
    result = parse_dates('day after tomorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2


def test_parse_dates_overmorrow():
    result = parse_dates('overmorrow')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].cardinality == 2
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_till_date():
    result = parse_dates('till date')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].tense == 'present'


def test_parse_dates_to_date():
    result = parse_dates('to date')
    assert len(result.relative_times) == 1
    assert result.relative_times[0].tense == 'present'


# =============================================================================
# Section 16: extract_relative_times API — all expressions
# =============================================================================

def test_extract_relative_the_day_before_yesterday():
    result = extract_relative_times('the day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_extract_relative_day_before_yesterday():
    result = extract_relative_times('day before yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_extract_relative_the_day_after_tomorrow():
    result = extract_relative_times('the day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_extract_relative_day_after_tomorrow():
    result = extract_relative_times('day after tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2


def test_extract_relative_overmorrow():
    result = extract_relative_times('overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_extract_relative_till_date():
    result = extract_relative_times('till date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


def test_extract_relative_to_date():
    result = extract_relative_times('to date')
    assert len(result) == 1
    assert result[0].cardinality == 0
    assert result[0].tense == 'present'


# =============================================================================
# Section 17: Additional sentence context variations
# =============================================================================

def test_sentence_capitalized_the_day_before_yesterday():
    result = parse_time_references('He called The Day Before Yesterday')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'past'


def test_sentence_capitalized_overmorrow():
    result = parse_time_references('Delivery expected Overmorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_sentence_capitalized_till_date():
    result = parse_time_references('Data collected Till Date is incomplete')
    assert len(result) == 1
    assert result[0].tense == 'present'


def test_sentence_day_after_tomorrow_capitalized():
    result = parse_time_references('Flight departs Day After Tomorrow')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].tense == 'future'


def test_sentence_to_date_business_context():
    result = parse_time_references('all transactions to date have been verified')
    assert len(result) == 1
    assert result[0].tense == 'present'


# =============================================================================
# Section 18: Cardinality type assertions
# =============================================================================

def test_cardinality_type_the_day_before_yesterday():
    result = parse_time_references('the day before yesterday')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_the_day_after_tomorrow():
    result = parse_time_references('the day after tomorrow')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_overmorrow():
    result = parse_time_references('overmorrow')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_till_date():
    result = parse_time_references('till date')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_to_date():
    result = parse_time_references('to date')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_day_before_yesterday():
    result = parse_time_references('day before yesterday')
    assert isinstance(result[0].cardinality, int)


def test_cardinality_type_day_after_tomorrow():
    result = parse_time_references('day after tomorrow')
    assert isinstance(result[0].cardinality, int)


def test_result_count_all_idioms_return_exactly_one():
    for expr in [
        'the day before yesterday',
        'day before yesterday',
        'the day after tomorrow',
        'day after tomorrow',
        'overmorrow',
        'till date',
        'to date',
    ]:
        result = parse_time_references(expr)
        assert len(result) == 1, f'Expected 1 result for {expr!r}, got {len(result)}'
